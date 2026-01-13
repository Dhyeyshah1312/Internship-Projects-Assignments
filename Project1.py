# Project: Climate & Public Health Analytics


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

print("Dataset loaded")
print(df.head())
print(df.info())



print("\nMissing values before cleaning:")
print(df.isnull().sum())


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

# Convert date column
df["week_start_date"] = pd.to_datetime(df["week_start_date"])

# Convert temperature
df["air_temp_c"] = df["reanalysis_air_temp_k"] - 273.15

print("\nMissing values after cleaning:")
print(df.isnull().sum())


print("\nBasic statistics:")
print(df.describe())

print("\nAverage cases by city:")
for city in df["city"].unique():
    avg = df[df["city"] == city]["total_cases"].mean()
    print(city, ":", avg)


print("\nCorrelation with total cases:")
print(df.corr(numeric_only=True)["total_cases"])



city_name = df["city"].iloc[0]
city_data = df[df["city"] == city_name]

plt.plot(city_data["week_start_date"], city_data["total_cases"])
plt.title("Disease Cases Over Time - " + city_name)
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.show()

plt.plot(city_data["week_start_date"], city_data["air_temp_c"])
plt.title("Temperature Over Time - " + city_name)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.show()




sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Heatmap")
plt.show()

df["rain_lag"] = df["precipitation_amt_mm"].shift(2)
print("\nLag effect correlation:")
print(df[["total_cases", "rain_lag"]].corr())

print("\nProject completed.")
