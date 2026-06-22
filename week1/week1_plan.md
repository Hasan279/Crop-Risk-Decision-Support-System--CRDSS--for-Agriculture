# Week 1 Step-by-Step Guide: Getting Data and Finding Risks

This guide will show you step-by-step how to download weather data and calculate the crop risks (Frost, Heat Stress, Heavy Rain). 

## Important Note Before We Start

> [!IMPORTANT]
> Please check these numbers to see if they are correct for your project:
> 1. We will use data for the last **20 years** (2004 to 2023). 
> 2. **Frost** is when the lowest temperature is $0°C$ or less.
> 3. **Heat Stress** is when the highest temperature is more than $35°C$ for 3 days in a row.
> 4. **Heavy Rain** is when it rains more than $50mm$ over 3 days.
> 
> Let me know if you want to change any of these numbers. If they are okay, you can start the steps below!

---

## Step 1: Create a Data Folder
1. Inside your project folder, create a new folder called `data`. This is where we will save our files.

## Step 2: Download Weather Data
1. Create a new Python file called `data_ingestion.py`.
2. In this file, write code to do the following:
   - Import the `requests` and `pandas` libraries.
   - List the GPS coordinates (latitude and longitude) for 5 cities: Multan, Hyderabad, Peshawar, Quetta, and Gilgit.
   - Use the Open-Meteo API to download daily weather data for the last 20 years for these 5 cities. You need to ask for:
     - Maximum daily temperature (`temperature_2m_max`)
     - Minimum daily temperature (`temperature_2m_min`)
     - Total daily rain (`precipitation_sum`)
   - Turn the downloaded data into a Pandas DataFrame.
   - Combine the data for all 5 cities into one big table.
   - Save this big table as a file called `historical_weather.csv` inside your `data` folder.

## Step 3: Calculate Crop Risks
1. Create a new Python file called `target_engineering.py`.
2. In this file, write code to do the following:
   - Import the `pandas` library.
   - Load the `historical_weather.csv` file you created in Step 2.
   - Find **Frost events**: Add a column that shows if the minimum temperature was $0°C$ or less on that day.
   - Find **Heat Stress events**: Add a column that shows if the maximum temperature was over $35°C$ for the past 3 days in a row.
   - Find **Heavy Rain events**: Add a column that adds up the rain for the past 3 days, and shows if the total is over $50mm$.
   - Save this updated table with the new risk columns as a file called `engineered_features.csv` inside your `data` folder.

## Step 4: Make Graphs
1. Create a new Jupyter Notebook file called `week1_exploration.ipynb`.
2. In this notebook, write code to do the following:
   - Load the `engineered_features.csv` file.
   - Make simple graphs (like bar charts or line graphs) to show:
     - How many times frost happened in each city over the years.
     - How many heatwaves happened in each city over the years.
     - How many heavy rain events happened in each city over the years.

## Step 5: Check Your Work
1. Open the `historical_weather.csv` and `engineered_features.csv` files and check that they look correct. Make sure there are no empty spots (NaNs).
2. Look at your graphs in the notebook. Does the data make sense? (For example, Gilgit should have more frost than Hyderabad).
