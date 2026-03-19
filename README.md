# Nairobi Traffic Congestion Prediction 🚗🇰🇪

## 📌 Problem Statement
Nairobi’s road network suffers from severe, unpredictable congestion that leads to significant economic loss. Current navigation tools offer real-time data but lack predictive depth regarding local "friction factors." This project develops a machine learning model to predict directional traffic congestion (levels 0–3) by analyzing the intersection of weather, matatu density, and the school calendar—specifically targeting **"Transition Weeks"** (opening, closing, and midterms) which represent the city's peak gridlock periods.

---

## 📊 Dataset Sources
The model is built on a multi-source "Feature Bank" to capture the complexity of Nairobi traffic:

* **Target Variable (Congestion):** A hybrid ground-truth dataset combining **TomTom Traffic Stats** (historical speed ratios) and primary data collection via **Google Maps Typical Traffic** (manual labeling of 21 segments at 2-hour intervals).
* **Public Transport (GTFS):** Route and stop density from the **Digital Matatus** dataset to quantify "commuter friction" at major stages.
* **Infrastructure (OSM):** Structural road data (lanes, road types, and node coordinates) extracted via **OpenStreetMap**.
* **Environmental (Weather):** Hourly precipitation and temperature data from the **Open-Meteo API**.
* **Temporal (School Calendar):** 2025 Ministry of Education dates, engineered to flag "High-Impact" weeks (Midterms, Opening, and Closing).

---

## ⚙️ Proposed Approach & Modeling Techniques
We are implementing a supervised learning pipeline in Python:

1.  **Feature Engineering:** Encoding the school calendar into an ordinal "Impact Level" (0–2) and calculating spatial matatu density within a 150m buffer of road segments.
2.  **Spatial Matching:** Linking manual Google Map landmarks to OpenStreetMap Node IDs ($u, v$) using coordinate-based joins.
3.  **Modeling:** * **Random Forest / XGBoost Regressors:** Chosen for their ability to handle non-linear relationships (e.g., the compounding effect of rain during a school opening week).
    * **Ordinal Classification:** Binning traffic into four distinct levels: **0** (Free-flow), **1** (Moderate), **2** (Heavy), and **3** (Gridlock).
4.  **Evaluation:** Using a temporal train/test split. Performance is measured using **Mean Absolute Error (MAE)** and **F1-Score**.

---

## 🚀 Expected Outcomes
* **Predictive Tool:** A model capable of forecasting congestion levels for specific road segments based on future date/time and weather forecasts.
* **Bottleneck Analysis:** Identification of the primary drivers of traffic (e.g., quantifying how much a "Midterm Week" increases travel time).
* **Data Strategy:** A proof-of-concept demonstrating how manual labeling of "Typical Traffic" can effectively augment official data in emerging markets.
