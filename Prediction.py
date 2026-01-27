from fastapi import FastAPI
import pandas as pd


# Initialized FastAPI app

app = FastAPI(title="Climate & Public Health Analytics API")


# Load and prepare data (from Climate Project )

df = pd.read_csv("data.csv")

# Converted date column
df["week_start_date"] = pd.to_datetime(df["week_start_date"])

# Handled missing values 
df["reanalysis_air_temp_k"] = df["reanalysis_air_temp_k"].fillna(
    df["reanalysis_air_temp_k"].mean()
)

df["reanalysis_specific_humidity_g_per_kg"] = df[
    "reanalysis_specific_humidity_g_per_kg"
].fillna(
    df["reanalysis_specific_humidity_g_per_kg"].mean()
)

df["precipitation_amt_mm"] = df["precipitation_amt_mm"].fillna(
    df["precipitation_amt_mm"].median()
)

# To Convert temperature from Kelvin to Celsius
df["air_temp_c"] = df["reanalysis_air_temp_k"] - 273.15

# Sort by date to ensure correct time order
df = df.sort_values("week_start_date")


# BASIC REST API (For Health Check)

@app.get("/")
def home():
    return {
        "message": "Climate & Public Health Prediction API is running"
    }


# CORE API: Predicted next 12 weeks

@app.get("/predict/12-weeks")
def predict_next_12_weeks():
    """
    Predict disease cases for the next 12 weeks
    using average trend of the past 52 weeks
    """

    # Took past 52 weeks of data
    last_52_weeks = df.tail(52)

    # Calculated average weekly cases
    avg_cases = last_52_weeks["total_cases"].mean()

    # Generated prediction for next 12 weeks
    predictions = []
    for week in range(1, 13):
        predictions.append({
            "week": week,
            "predicted_cases": int(avg_cases)
        })

    return {
        "prediction_method": "Trend-based average of past 52 weeks",
        "weeks_used_for_analysis": 52,
        "forecast_horizon_weeks": 12,
        "predictions": predictions
    }



#Links to test the swagger api: http://127.0.0.1:8000/docs#/  &  http://127.0.0.1:8000/predict/12-weeks
