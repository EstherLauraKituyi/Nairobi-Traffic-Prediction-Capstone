# Nairobi SmartTraffic AI 🚗🇰🇪
**A Predictive & Real-Time Traffic Management System for Nairobi's Road Networks**

## 📌 Project Overview
Nairobi SmartTraffic AI is a full-stack Machine Learning application developed to solve the unpredictability of urban congestion in Kenya. While traditional GPS tools provide real-time snapshots, this system bridges the gap by **predicting** future traffic states using a Random Forest model and providing **incident-aware routing** via Google Maps API integration.

This project was developed as part of a Data Science Traineeship, focusing on how "friction factors" like the school calendar and weather impact city-wide mobility.

---

## ⚙️ Technical Architecture

### 1. The Intelligence Layer (Machine Learning)
* **Model:** Random Forest Classifier (unpickled via `scikit-learn` in production).
* **Feature Engineering:** * **Temporal:** Hour of day, day of week, and "High-Impact" school calendar flags (Opening, Closing, and Midterms).
    * **Environmental:** Real-time temperature and precipitation data.
    * **Spatial:** Matatu density metrics within a 150m buffer of major road segments.
* **Target:** Ordinal Classification of traffic into four levels: **0** (Free-flow), **1** (Moderate), **2** (Heavy), and **3** (Gridlock).

### 2. The Navigation Layer (APIs)
* **Google Maps Platform:** Implemented `departure_time=now` to fetch live traffic conditions and incident-aware ETAs.
* **Dynamic Rerouting:** Enabled `alternatives=true` to provide users with multiple path options, visualized through dynamic layers.
* **Weather Integration:** Real-time data fetching to feed predictive input during live inference.

### 3. The Production Stack (DevOps)
* **Backend:** Django (Python)
* **Static Files:** Served via **WhiteNoise** for high-speed production delivery.
* **Deployment:** Managed via **Render** with a custom Gunicorn/WSGI configuration.
* **Security:** API keys and sensitive credentials managed through environment variables.

---

## 📊 Dataset Sources
The model is built on a multi-source "Feature Bank":
* **Target Variable:** A hybrid ground-truth dataset combining **TomTom Traffic Stats** and primary data collection via **Google Maps Typical Traffic**.
* **Public Transport (GTFS):** Route and stop density from the **Digital Matatus** dataset.
* **Infrastructure (OSM):** Structural road data extracted via **OpenStreetMap**.
* **Environmental:** Hourly precipitation/temperature from **Open-Meteo**.
* **Temporal:** 2025 Ministry of Education dates, engineered to flag "High-Impact" transition weeks.

---

## 🚀 Key Features
* **Predictive Dashboard:** Forecasts traffic levels based on time, weather, and school events.
* **Sleek ETA Widget:** A custom glowing dashboard showing live arrival times.
* **Interactive Map:**
    * **Primary Route:** Highlighted in bold for clarity.
    * **Alternative Routes:** Shown as dashed lines to help users avoid sudden gridlock.
* **Smart Advice:** AI-generated summaries to give drivers context on their route (e.g., "Standard volume for Nairobi").

---

## 🛠️ Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/nairobi-traffic-ai.git](https://github.com/YourUsername/nairobi-traffic-ai.git)
   cd nairobi-traffic-ai

   Install dependencies:


pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and add your keys:


GOOGLE_MAPS_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
SECRET_KEY=your_django_secret_key
Run the server:

Bash
python manage.py runserver
