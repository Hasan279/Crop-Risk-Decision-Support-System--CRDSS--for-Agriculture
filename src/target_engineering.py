import pandas as pd
import numpy as np

# Load the weather data
df = pd.read_csv("data/raw/historical_weather.csv")

# 1. Frost event (min temperature is < 2°C, or use <= 0°C as per plan)
df["frost_event"] = (df["temperature_2m_min"] < 2).astype(int)

# 2. Heat stress (max temperature > 35°C for 3 consecutive days)
# Grouping by city_id ensures rolling calculations don't bleed between different cities
df["heat_stress_event"] = (
    df.groupby("city_id")["temperature_2m_max"]
    .rolling(window=3)
    .min()
    .gt(35)
    .astype(int)
    .reset_index(level=0, drop=True)
)

# 3. Heavy rain (rain sum over 3 days > 50mm)
df["heavy_rain_event"] = (
    df.groupby("city_id")["precipitation_sum"]
    .rolling(window=3)
    .sum()
    .gt(50)
    .astype(int)
    .reset_index(level=0, drop=True)
)

# Fill NaNs from rolling windows with 0
df["heat_stress_event"] = df["heat_stress_event"].fillna(0).astype(int)
df["heavy_rain_event"] = df["heavy_rain_event"].fillna(0).astype(int)

# Save to the target CSV
df.to_csv("data/processed/engineered_features.csv", index=False)
print("Engineered features saved to data/engineered_features.csv")

# Verify unique values
print("\nUnique values in each target column:")
print(f"Frost Events: {np.unique(df['frost_event'], return_counts=True)}")
print(f"Heat Stress Events: {np.unique(df['heat_stress_event'], return_counts=True)}")
print(f"Heavy Rain Events: {np.unique(df['heavy_rain_event'], return_counts=True)}")
