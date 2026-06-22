import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import os

daily_vars = [
    "temperature_2m_max", 
    "temperature_2m_min", 
    "precipitation_sum", 
    "wind_speed_10m_max", 
    "shortwave_radiation_sum", 
    "et0_fao_evapotranspiration"
]

cities = [
	{
		"latitude": 30.03,
		"longitude": 70.64,
		"start_date": "2005-01-01",
		"end_date": "2026-01-01",
		"daily": daily_vars
	},
	{
		"latitude": 26.04,
		"longitude": 68.95,
		"start_date": "2005-01-01",
		"end_date": "2026-01-01",
		"daily": daily_vars
	},
	{
		"latitude": 32.07,
		"longitude": 73.69,
		"start_date": "2005-01-01",
		"end_date": "2026-01-01",
		"daily": daily_vars
	},
	{
		"latitude": 31.42,
		"longitude": 73.09,
		"start_date": "2005-01-01",
		"end_date": "2026-01-01",
		"daily": daily_vars
	},
	{
		"latitude": 30.81,
		"longitude": 73.45,
		"start_date": "2005-01-01",
		"end_date": "2026-01-01",
		"daily": daily_vars
	}
]

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

all_responses = []
for city_params in cities:
    res = openmeteo.weather_api(url, params=city_params)
    all_responses.extend(res)

all_dfs = []
for i, response in enumerate(all_responses):
    daily = response.Daily()
    
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(2).ValuesAsNumpy(),
        "wind_speed_10m_max": daily.Variables(3).ValuesAsNumpy(),
        "shortwave_radiation_sum": daily.Variables(4).ValuesAsNumpy(),
        "et0_fao_evapotranspiration": daily.Variables(5).ValuesAsNumpy()
    }
    
    df = pd.DataFrame(data=daily_data)
    # Add a city identifier based on index
    df["city_id"] = i + 1
    df["latitude"] = cities[i]["latitude"]
    df["longitude"] = cities[i]["longitude"]
    
    all_dfs.append(df)

# Combine all into one big dataframe
combined_df = pd.concat(all_dfs, ignore_index=True)

# Save to CSV
os.makedirs("data", exist_ok=True)
csv_path = os.path.join("data", "historical_weather.csv")
combined_df.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")