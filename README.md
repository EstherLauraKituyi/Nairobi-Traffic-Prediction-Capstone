# 🚗🇰🇪 Nairobi SmartTraffic AI 
**A Predictive & Real-Time Traffic Management System for Nairobi's Road Networks**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-Production-green)
![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-orange)
![Google Maps](https://img.shields.io/badge/API-Google_Maps-4285F4)

## 📌 Project Overview
Nairobi SmartTraffic AI is a full-stack Machine Learning application developed to solve the unpredictability of urban congestion in Kenya. While traditional GPS tools provide real-time snapshots, this system bridges the gap by **predicting future traffic states** using a Random Forest model, while also providing **incident-aware live routing** via dynamic API integrations.

This project was developed as a Capstone Data Science project, focusing heavily on how "friction factors"—such as the Kenyan school calendar, toll road economics, and sudden weather changes—impact city-wide mobility.

---

## ✨ Key Features & Capabilities

* **Dual-Mode AI Engine:** 
  * **"Leave Right Now" (Live Mode):** Silently fetches live local weather, injects real-time accident telemetry, and provides a live Estimated Time of Arrival (ETA).
  * **"Plan for Later" (Predictive Mode):** Allows users to input future variables (e.g., Next Monday at 5 PM with Heavy Rain) to forecast commute conditions.
* **Segment-Level Visual Diagnostics:** While the ML model predicts the overall *Trip-Level* congestion, the app injects **Google Maps Live Traffic Tiles** into the background. This allows users to visually break down exactly which segments of the road (Red/Yellow/Green) are causing the AI's "Severe" prediction.
* **Toll Economics (Expressway Toggle):** Users can choose to bypass the Nairobi Expressway. The system will dynamically reroute the underlying polyline to Mombasa Road/Waiyaki Way and recalculate transit friction.
* **Dynamic Alternative Routing:** The map draws the primary AI-predicted route in bold, while rendering 1-2 alternative routes in dashed grey, giving drivers visual backup options.
* **Premium "Smart City" UI/UX:** Built with modern Glassmorphism, dark mode aesthetics, an infinite-scrolling live ticker tape, and a glowing ETA dashboard widget.

---

## ⚙️ Technical Architecture

### 1. The Intelligence Layer (Machine Learning)
* **Model:** Random Forest Classifier (unpickled via `scikit-learn` in production).
* **Target:** Ordinal Classification of traffic into four states: **0** (`Clear`), **1** (`Moderate`), **2** (`Heavy`), and **3** (`Severe`).
* **Feature Engineering:** 
    * **Temporal:** Hour of day, day of week, and engineered flags for "High-Impact" school transition weeks (Opening/Closing terms).
    * **Environmental:** Real-time temperature and precipitation data.
    * **Spatial (Dynamic):** Matatu (Transit) density metrics calculated on-the-fly.

### 2. The Navigation & API Layer
* **Google Directions API:** Utilized `departure_time=now` for live accident awareness, and `alternatives=true` for multi-path rendering.
* **Google Places API:** Replaced static dataset buffers with dynamic queries to count transit stations (`type=transit_station`) within a 2km radius of the destination.
* **OpenWeatherMap API:** Real-time meteorological data fetching for live-inference inputs.
* **Folium:** Map rendering with custom User-Agent headers to bypass production blockades.

### 3. The Production Stack (DevOps)
* **Backend:** Django (Python).
* **Static Files:** Served via **WhiteNoise** for high-speed production delivery.
* **Deployment:** Hosted on **Render** utilizing a custom Gunicorn/WSGI configuration.
* **Security:** API keys and sensitive credentials strictly managed through environment variables (`.env`).

---

## 📊 Dataset Sources
The foundational model was trained on a multi-source "Feature Bank":
* **Target Variable:** A hybrid ground-truth dataset combining **TomTom Traffic Stats** and primary data collection via **Google Maps Typical Traffic**.
* **Public Transport (GTFS):** Baseline route and stop density sourced from the **Digital Matatus** project.
* **Infrastructure (OSM):** Structural road data extracted via **OpenStreetMap**.
* **Environmental:** Historical hourly precipitation/temperature from **Open-Meteo**.
* **Temporal:** 2025 Ministry of Education dates, engineered to flag peak "Friction Weeks".

---

## 🛠️ Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EstherLauraKituyi/Nairobi-Traffic-Prediction-Capstone.git
   cd Nairobi-Traffic-Prediction-Capstone
2. **Create a virtual environment & install dependencies:**
   ``` bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt

3. **Configure Environment Variables:**
Create a .env file in the root directory and add your API keys:
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
SECRET_KEY=your_django_secret_key_here

5. **Run the server:**
```bash
python manage.py runserver

6. ** Navigate to http://127.0.0.1:8000 in your browser to view the app!**
