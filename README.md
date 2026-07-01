# 🌱 Crop Risk Decision Support System (CRDSS) for Agriculture

An intelligent, interactive decision-support application designed to help agricultural professionals assess weather-related risks (like heat stress, frost, and heavy rain) before making critical planting decisions. The system is tailored for major agricultural hubs in Pakistan and provides comprehensive risk analysis for various crops.

## ✨ Features

- **📊 Probabilistic Risk Engine**: Calculates the statistical likelihood of adverse weather events across critical growth stages by analyzing historical meteorological data.
- **🌾 Agronomic Knowledge Base**: Embedded rules for major crops (`Wheat`, `Cotton`, `Rice`, `Sugarcane`, `Maize`) to cross-reference plant vulnerabilities with weather forecasts.
- **🌍 Bilingual Interface (English & اردو)**: Fully localized UI, dynamically translating risk warnings, crop names, and charts into standard Urdu (using the *Noto Nastaliq Urdu* font) for superior accessibility in local agriculture.
- **🎨 Premium Interactive Dashboard**: A completely redesigned, nature-inspired UI built with Streamlit. Features modern typography (*DM Sans*), a bespoke design system with refined colors (Forest, Fern, Sage), polished KPI cards, and beautifully integrated Plotly charts with transparent backgrounds and smooth curves.
- **📓 Data Exploration**: Includes Jupyter Notebooks for transparent Exploratory Data Analysis (EDA) on weather features and risk distributions.

## 🧠 Data & Model Architecture

### Why These Regions?
The system focuses on five major agricultural hubs in Pakistan—**Dera Ghazi Khan, Sanghar, Hafizabad, Faisalabad, and Okara**. These cities were strategically selected because they represent distinct agro-ecological zones and are the primary producers of Pakistan's major cash and food crops (Wheat, Cotton, Rice, Sugarcane, Maize). 

### Data Processing & Risk Thresholds
Instead of using raw weather averages, the data pipeline engineers specific **agrometeorological risk events** based on biological crop stress thresholds:
- **Heat Stress:** Maximum temperature exceeding 35°C for 3 consecutive days.
- **Heavy Rain:** Precipitation accumulating to more than 50mm over a rolling 3-day window.
- **Frost:** Minimum temperature dropping below 2°C.

### The Probabilistic Model
Rather than a black-box machine learning classifier, we implemented a **Time-Weighted Empirical Probability Model**. 
- **Interpretability:** This approach provides a clear, statistically grounded percentage (e.g., "30% chance of heat stress") that is easily interpretable by farmers and agronomists.
- **Climate Change Adjustment:** Weather patterns from 20 years ago are less representative today. The model applies a heavier weight (2.0x) to events occurring in the most recent 5 years. This allows the system to adapt to recent climate shifts and increasing extreme weather anomalies without sacrificing the statistical stability of a 20-year baseline.

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Custom CSS
- **Data Visualization**: Plotly Express, Plotly Graph Objects
- **Data Engineering & Modeling**: Python, Pandas, NumPy

## 📁 Project Structure

```text
├── .streamlit/             # Streamlit configuration and theme settings
├── data/
│   ├── raw/                # Original historical weather data
│   └── processed/          # Engineered features and calculated risk probabilities
├── docs/                   # Software Requirements Specification (SRS)
├── notebooks/              # Jupyter Notebooks (e.g., Exploratory Data Analysis)
├── src/                    # Core backend modules
│   ├── agronomic_rules.py  # Crop-specific logic and AI recommendation engine
│   ├── data_pipeline.py    # ETL scripts for cleaning and imputing weather data
│   └── probabilistic_model.py # Statistical models calculating daily risk thresholds
├── app.py                  # Main Streamlit web application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🚀 Installation & Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/crop-risk-dss.git
   cd crop-risk-dss
   ```

2. **Install Dependencies**
   Ensure you have Python 3.9+ installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Data Pipeline (If data is missing)**
   Process the raw weather data and generate the risk probabilities.
   ```bash
   python src/data_pipeline.py
   python src/probabilistic_model.py
   ```

4. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

## 🎯 How It Works

1. **Select Parameters**: Choose your city, the crop you intend to plant, and your target planting date from the sidebar.
2. **Set the Horizon**: Choose how many days of historical data the probabilistic model should evaluate (e.g., 30 Days).
3. **Analyze**: The app renders an interactive chart showing the exact day of the year your crop hits vulnerable growth stages and maps it against the probability of severe weather.
4. **Get Advice**: Read the generated farming advice at the bottom. Switch the language toggle to `اردو` to instantly translate the UI and the generated recommendations.

## 📄 License
This project is licensed under the MIT License.
