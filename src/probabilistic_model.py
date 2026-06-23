import pandas as pd
import numpy as np
from pathlib import Path

def generate_risk_probabilities():
    # Build the path dynamically so it works no matter where the script is run from
    current_dir = Path(__file__).resolve().parent
    data_path = current_dir.parent / "data" / "processed" / "engineered_features.csv"
    output_path = current_dir.parent / "data" / "processed" / "risk_probabilities.csv"
    
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    print("Processing dates...")
    df['date'] = pd.to_datetime(df['date'])
    df['DOY'] = df['date'].dt.dayofyear
    df['Year'] = df['date'].dt.year
    
    # Sort to ensure chronological order for rolling windows
    df.sort_values(by=['city_name', 'date'], inplace=True)
    
    # Define parameters
    risk_cols = ['frost_event', 'heat_stress_event', 'heavy_rain_event']
    window_sizes = [15, 30, 45, 60, 90]
    
    # Calculate Climate Shift Weights (give last 5 years a weight of 2.0, others 1.0)
    years = sorted(df['Year'].unique())
    recent_years = years[-5:]
    weight_map = {y: 2.0 if y in recent_years else 1.0 for y in years}
    df['weight'] = df['Year'].map(weight_map)
    
    print("Computing forward-looking events using rolling windows...")
    for window in window_sizes:
        # FixedForwardWindowIndexer looks at the current day + (window-1) future days
        indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=window)
        for risk in risk_cols:
            col_name = f"{risk}_{window}d"
            df[col_name] = df.groupby('city_name')[risk].rolling(window=indexer).max().reset_index(0, drop=True)
    
    print("Aggregating historical probabilities...")
    records = []
    # Group by City and DOY
    grouped = df.groupby(['city_name', 'DOY'])
    
    for (city, doy), subset in grouped:
        total_weight = subset['weight'].sum()
        if total_weight == 0:
            continue
            
        for window in window_sizes:
            for risk in risk_cols:
                col_name = f"{risk}_{window}d"
                # Weighted probability = sum(event_occurred * weight) / sum(weights)
                prob = (subset[col_name] * subset['weight']).sum() / total_weight
                
                records.append({
                    'city_name': city,
                    'DOY': doy,
                    'risk_type': risk.replace('_event', ''),
                    'window_days': window,
                    'probability': round(prob, 4)
                })

    final_df = pd.DataFrame(records)
    
    # Ensure directory exists before saving
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False)
    print(f"Successfully saved probabilities to: {output_path}")

if __name__ == "__main__":
    generate_risk_probabilities()