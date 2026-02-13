from fastapi import FastAPI, Query
import pandas as pd
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA

app = FastAPI(title="Climate & Public Health Prediction API")

# Loaded data
df = pd.read_csv("data.csv")
df["week_start_date"] = pd.to_datetime(df["week_start_date"], dayfirst=True)

# Used single city
city_name = df["city"].iloc[0]
df_city = df[df["city"] == city_name].sort_values("week_start_date")

# Last 52 weeks 
last_52_weeks = df_city.tail(52)


# Health Check

@app.get("/")
def home():
    return {
        "message": "Prediction API is running",
        "city": city_name
    }


# Unified Prediction Endpoint
@app.get("/predict/12-weeks")
def predict_next_12_weeks(
    model: str = Query("prophet", enum=["prophet", "arima"])
):


 # PROPHET
   
    if model == "prophet":
        prophet_df = last_52_weeks.rename(
            columns={"week_start_date": "ds", "total_cases": "y"}
        )

        m = Prophet(yearly_seasonality=True, weekly_seasonality=False)
        m.fit(prophet_df)

        future = m.make_future_dataframe(periods=12, freq="W")
        forecast = m.predict(future)
        forecast_12 = forecast.tail(12)

        predictions = [
            {
                "week": row["ds"].strftime("%Y-%m-%d"),
                "predicted_cases": int(round(max(row["yhat"], 0)))
            }
            for _, row in forecast_12.iterrows()
        ]

    
    # ARIMA
    
    elif model == "arima":

        series = last_52_weeks["total_cases"].values

        arima_model = ARIMA(series, order=(1, 1, 1))
        arima_result = arima_model.fit()

        forecast = arima_result.forecast(steps=12)

        last_date = last_52_weeks["week_start_date"].iloc[-1]
        future_dates = pd.date_range(
            start=last_date,
            periods=13,
            freq="W"
        )[1:]

        predictions = [
            {
                "week": future_dates[i].strftime("%Y-%m-%d"),
                "predicted_cases": int(round(max(forecast[i], 0)))
            }
            for i in range(12)
        ]

    return {
        "model_used": model,
        "training_window_weeks": 52,
        "forecast_horizon_weeks": 12,
        "city": city_name,
        "predictions": predictions
    }
