import os
import joblib
import pandas as pd
import folium
import requests
import polyline
import datetime
from dotenv import load_dotenv
from django.shortcuts import render
from django.conf import settings

# 1. LOAD Environment Variables
load_dotenv()

# 2. LOAD trained model and scaler
MODEL_PATH = os.path.join(settings.BASE_DIR, 'traffic_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"⚠️ Model Loading Error: {e}")

# 3. API KEYS
GOOGLE_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')

def predict_traffic(request):
    if request.method == 'POST':
        try:
            # --- EXTRACT ROUTE COORDINATES ---
            to_lat_raw = request.POST.get('to_lat')
            to_lon_raw = request.POST.get('to_lon')

            if not to_lat_raw or not to_lon_raw:
                return render(request, 'predictor/index.html', {
                    'error': "Missing destination coordinates. Please select a valid location from the dropdown.",
                    'google_key': GOOGLE_API_KEY
                })

            from_lat = float(request.POST.get('from_lat', -1.279))
            from_lon = float(request.POST.get('from_lon', 36.817))
            to_lat = float(to_lat_raw)
            to_lon = float(to_lon_raw)
            
            # --- NEW TOGGLES ---
            school_impact = 1 if request.POST.get('school_impact') else 0
            avoid_expressway = True if request.POST.get('avoid_expressway') else False
            timing_mode = request.POST.get('timing_mode', 'now')

            # --- DYNAMIC TIME & WEATHER LOGIC ---
            if timing_mode == 'now':
                # 1. Get Live Local Time
                now = datetime.datetime.now()
                hour = now.hour
                day = now.weekday() # Monday = 0, Sunday = 6
                
                # 2. Get Live Weather for the Route Origin
                temp_c = 22.0 # Default fallback
                rain_mm = 0.0 # Default fallback
                
                if OPENWEATHER_API_KEY:
                    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={from_lat}&lon={from_lon}&appid={OPENWEATHER_API_KEY}&units=metric"
                    try:
                        w_res = requests.get(weather_url, timeout=3).json()
                        temp_c = w_res.get('main', {}).get('temp', 22.0)
                        # OpenWeather returns rain volume for the last 1 hour if it is raining
                        rain_dict = w_res.get('rain', {})
                        rain_mm = rain_dict.get('1h', 0.0)
                    except:
                        pass # Silently fallback to defaults if API fails
            else:
                # User selected "Plan for Later", use their manual inputs
                hour = int(request.POST.get('hour', 8))
                day = int(request.POST.get('day', 0))
                rain_mm = float(request.POST.get('rain', 0.0))
                temp_c = 22.0 # Standard average for future planning

            # --- DYNAMIC MATATU STOP COUNT (Places API) ---
            # Searches for transit stations within 2km of the destination
            matatu_stop_count = 5 # Fallback
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={to_lat},{to_lon}&radius=2000&type=transit_station&key={GOOGLE_API_KEY}"
            try:
                p_res = requests.get(places_url, timeout=3).json()
                if p_res.get('status') == 'OK':
                    # Count how many stations Google found (max 20 per request)
                    found_stops = len(p_res.get('results', []))
                    if found_stops > 0:
                        matatu_stop_count = found_stops
            except:
                pass

            # --- FEATURE ENGINEERING ---
            is_weekend = 1 if day >= 5 else 0
            is_peak_hour = 1 if hour in [7, 8, 9, 16, 17, 18, 19] else 0
            
            data = {
                'from_lat': from_lat,
                'from_lon': from_lon,
                'to_lat': to_lat,
                'to_lon': to_lon,
                'matatu_stop_count': matatu_stop_count, # Now dynamic!
                'is_inbound': 1,
                'hour': hour,
                'day_of_week_enc': day,
                'is_weekend': is_weekend,
                'is_peak_hour': is_peak_hour,
                'school_impact': school_impact, # Now dynamic!
                'avg_rain_mm': rain_mm,         # Now dynamic!
                'avg_temp_c': temp_c            # Now dynamic!
            }

            # --- AI PREDICTION LOGIC ---
            input_df = pd.DataFrame([data])
            scaled_data = scaler.transform(input_df)
            
            prediction_num = model.predict(scaled_data)[0]
            probabilities = model.predict_proba(scaled_data)[0]
            confidence_score = max(probabilities) * 100 

            labels = {0: 'Clear', 1: 'Moderate', 2: 'Heavy', 3: 'Severe'}
            colors = {0: '#10b981', 1: '#f59e0b', 2: '#f97316', 3: '#ef4444'} 
            
            prediction_text = labels.get(prediction_num, 'Unknown')
            line_color = colors.get(prediction_num, '#3b82f6')

            # --- MAPPING (Folium + Google Directions) ---
            # 1. Create base map with NO default tiles to avoid OSM block
            m = folium.Map(location=[(from_lat + to_lat)/2, (from_lon + to_lon)/2], zoom_start=13, zoom_control=False, tiles=None)
            
            # 2. Add custom TileLayer with User-Agent to satisfy Render/OSM requirements
            folium.TileLayer(
                tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                headers={'User-Agent': 'NairobiTrafficAI/1.0 (Contact: lauramukite25@gmail.com)'} # <-- UPDATE EMAIL
            ).add_to(m)

            # --- GOOGLE DIRECTIONS WITH TOLL AVOIDANCE ---
            directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={from_lat},{from_lon}&destination={to_lat},{to_lon}&key={GOOGLE_API_KEY}"
            
            # If user checked "Avoid Expressway", tell Google to avoid tolls!
            if avoid_expressway:
                directions_url += "&avoid=tolls"

            route_response = requests.get(directions_url).json()

            if route_response.get('status') == 'OK':
                encoded_polyline = route_response['routes'][0]['overview_polyline']['points']
                road_coordinates = polyline.decode(encoded_polyline)
                
                folium.PolyLine(
                    road_coordinates,
                    color=line_color,
                    weight=8,
                    opacity=0.9,
                    tooltip=f"Predicted Flow: {prediction_text}"
                ).add_to(m)
                
                folium.Marker([from_lat, from_lon], popup="Start", icon=folium.Icon(color='darkblue', icon='circle')).add_to(m)
                folium.Marker([to_lat, to_lon], popup="Destination", icon=folium.Icon(color='red', icon='flag')).add_to(m)
                
                m.fit_bounds([ [min(p[0] for p in road_coordinates), min(p[1] for p in road_coordinates)], 
                               [max(p[0] for p in road_coordinates), max(p[1] for p in road_coordinates)] ])
            else:
                folium.PolyLine([(from_lat, from_lon), (to_lat, to_lon)], color=line_color, weight=5).add_to(m)

            map_html = m.get_root().render()

            # --- RENDER RESULTS ---
            return render(request, 'predictor/result.html', {
                'prediction': prediction_text,
                'confidence': round(confidence_score, 1),
                'map_html': map_html,
                'google_key': GOOGLE_API_KEY 
            })

        except Exception as e:
            return render(request, 'predictor/index.html', {
                'error': f"Prediction failed: {str(e)}",
                'google_key': GOOGLE_API_KEY
            })

    return render(request, 'predictor/index.html', {'google_key': GOOGLE_API_KEY})