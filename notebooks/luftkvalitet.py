import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Definer API og parametere
url = "https://api.met.no/weatherapi/airqualityforecast/0.1/"
params = {
    "lat": 60,
    "lon": 10,
    "areaclass": "grunnkrets"
}
headers = {"User-Agent": "MyAirQualityApp/1.0 (westersjoserina@gmail.com)"}

# Hent data fra API-en
response = requests.get(url, params=params, headers=headers)
if response.status_code != 200:
    print("Feil ved henting av data:", response.status_code)
    exit()

data = response.json()

#finner tid
time_entries = data.get("data", {}).get("time", [])

#lager liste for tidspunkter og AQI-parametrene fra API-en som vi ville hente
times = []
aqi = []
aqi_no2 = []
aqi_pm10 = []
aqi_pm25 = []
aqi_o3 = []

for entry in time_entries:
    from_time_str = entry.get("from")
    dt = datetime.datetime.strptime(from_time_str, "%Y-%m-%dT%H:%M:%SZ")
    times.append(dt)
    variables = entry.get("variables", {})
    aqi.append(variables.get("AQI", {}).get("value", None))
    aqi_no2.append(variables.get("AQI_no2", {}).get("value", None))
    aqi_pm10.append(variables.get("AQI_pm10", {}).get("value", None))
    aqi_pm25.append(variables.get("AQI_pm25", {}).get("value", None))
    aqi_o3.append(variables.get("AQI_o3", {}).get("value", None))

#lager en DataFrame for enklere håndtering
df = pd.DataFrame({
    "Time": times,
    "AQI": aqi,
    "AQI_no2": aqi_no2,
    "AQI_pm10": aqi_pm10,
    "AQI_pm25": aqi_pm25,
    "AQI_o3": aqi_o3
})
df.sort_values("Time", inplace=True)
df.set_index("Time", inplace=True)

#bruker Matplotlib og Seaborn for plotting
sns.set(style="whitegrid")
plt.figure(figsize=(12,6))
plt.plot(df.index, df["AQI"], marker='o', label="AQI")
plt.plot(df.index, df["AQI_no2"], marker='o', label="NO2")
plt.plot(df.index, df["AQI_pm10"], marker='o', label="pm10")
plt.plot(df.index, df["AQI_pm25"], marker='o', label="pm25")
plt.plot(df.index, df["AQI_o3"], marker='o', label="O3")
plt.xlabel("Dato og tidspunkt")
plt.ylabel("Luftkvalitetsindeks (AQI)")
plt.title("Luftkvalitetsprognose over tid")
plt.xticks(rotation=45)
plt.legend()

#endring av klokkeslett og tid for at det skal se bedre ut
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))

plt.tight_layout()
plt.show()
