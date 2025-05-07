import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

def luftkvalitet():
    #Definerer API og parametere
    url = "https://api.met.no/weatherapi/airqualityforecast/0.1/"
    params = {
        "lat": 60,
        "lon": 10,
        "areaclass": "grunnkrets"
    }
    headers = {"User-Agent": "MyAirQualityApp/1.0 (westersjoserina@gmail.com)"}
    #Henter data fra API-en
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("Feil ved henting av data:", response.status_code)
        return

    data = response.json()
    #Finner tid
    time_entries = data.get("data", {}).get("time", [])

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
#Lager en DataFrame for enklere håndtering
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

#Bruker Matplotlib og Seaborn for plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["AQI"], marker='o', label="AQI")
    plt.plot(df.index, df["AQI_no2"], marker='o', label="NO2")
    plt.plot(df.index, df["AQI_pm10"], marker='o', label="PM10")
    plt.plot(df.index, df["AQI_pm25"], marker='o', label="PM2.5")
    plt.plot(df.index, df["AQI_o3"], marker='o', label="O3")

    plt.xlabel("Dato og tidspunkt")
    plt.ylabel("Luftkvalitetsindeks (AQI)")
    plt.title("Luftkvalitetsprognose over tid")
    plt.xticks(rotation=45)
    plt.legend()
#Endring av klokkeslett og tid for at det skal se bedre ut
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    plt.tight_layout()
    plt.show()

#For testing
if __name__ == "__main__":
    luftkvalitet()
