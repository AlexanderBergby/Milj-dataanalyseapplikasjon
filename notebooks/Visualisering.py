# ------------------------------------
# 1. Importer nødvendige biblioteker
# ------------------------------------
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ------------------------------------
# 2. Hent værdata via Frost API
# ------------------------------------
print("Henter værdata...")

client_id = "e1e74478-764e-4bac-8a69-f70fe2ed8c6d"
observations_url = "https://frost.met.no/observations/v0.jsonld"
valgt_stasjon = "SN68090"  # Trondheim - Granåsen
temperatur_element = "air_temperature"
nedbør_element = "sum(precipitation_amount P1D)"
vindhastighet_element = "wind_speed"

idag = datetime.now(timezone.utc).date()
start_dato = (idag - timedelta(days=21)).strftime("%Y-%m-%d")  # 21 dager tilbake
slutt_dato = idag.strftime("%Y-%m-%d")

params = {
    "sources": valgt_stasjon,
    "elements": f"{temperatur_element},{nedbør_element},{vindhastighet_element}",
    "referencetime": f"{start_dato}/{slutt_dato}"
}

response = requests.get(observations_url, params=params, auth=(client_id, ""))
data = response.json()["data"] if response.status_code == 200 else []

temperatur_data, nedbør_data, vind_data = {}, {}, {}

for entry in data:
    dato = entry["referenceTime"][:10]
    for obs in entry["observations"]:
        verdi = obs["value"]
        element = obs["elementId"]
        if element == temperatur_element:
            temperatur_data.setdefault(dato, []).append(verdi)
        if element == nedbør_element:
            nedbør_data[dato] = nedbør_data.get(dato, 0) + verdi
        if element == vindhastighet_element:
            vind_data.setdefault(dato, []).append(verdi)

weather_rows = []
for dato in sorted(temperatur_data.keys()):
    avg_temp = round(np.mean(temperatur_data[dato]), 2)
    nedbør_mengde = nedbør_data.get(dato, 0)
    avg_vind = round(np.mean(vind_data[dato]), 2) if dato in vind_data else None
    weather_rows.append({"date": dato, "avg_temp": avg_temp, "precipitation": nedbør_mengde, "wind_speed": avg_vind})

weather_df = pd.DataFrame(weather_rows)
weather_df['date'] = pd.to_datetime(weather_df['date']).dt.date
print("\nVærdata:\n", weather_df.head())

# ------------------------------------
# 3. Hent historiske NILU-data
# ------------------------------------
print("\nHenter historiske luftkvalitetsdata fra NILU...")

nilu_url = "https://api.nilu.no/obs/historical"
nilu_params = {
    "components": "PM10,NO2,O3",
    "stations": "Trondheim",
    "fromDate": (idag - timedelta(days=21)).strftime("%Y-%m-%d"),
    "toDate": idag.strftime("%Y-%m-%d")
}

response = requests.get(nilu_url, params=nilu_params)
if response.status_code == 200:
    data = response.json()
    print(f"Antall NILU-målinger hentet: {len(data)}")
else:
    print("Feil ved henting av NILU-data:", response.status_code)
    data = []

rows = []
for entry in data:
    date = entry['fromTime'][:10]
    component = entry['component']
    value = entry['value']
    rows.append({'date': date, 'component': component, 'value': value})

df = pd.DataFrame(rows)
relevante_komponenter = ['PM10', 'NO2', 'O3']
df = df[df['component'].isin(relevante_komponenter)]

df_pivot = df.pivot_table(index='date', columns='component', values='value', aggfunc='mean').reset_index()
df_pivot.columns.name = None
df_pivot['date'] = pd.to_datetime(df_pivot['date']).dt.date
print("\nLuftkvalitetsdata fra NILU:\n", df_pivot.head())

# ------------------------------------
# 4. Slå sammen data
# ------------------------------------
print("\nSlår sammen vær- og luftkvalitetsdata...")

combined_df = pd.merge(weather_df, df_pivot, on='date', how='inner')
print("\nSammenslått datasett:\n", combined_df.head())

# ------------------------------------
# 5. Tren lineær regresjonsmodell (forutsi PM10)
# ------------------------------------
print("\nTrener prediktiv modell for PM10...")

X = combined_df[['avg_temp', 'precipitation', 'wind_speed']].fillna(0)  # Features
y = combined_df['PM10']  # Target

# Kun hvis vi har nok data
if len(combined_df) > 5:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # ------------------------------------
    # 6. Evaluer modellen
    # ------------------------------------
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nModell-evaluering:\nMean Squared Error (MSE): {mse:.2f}\nR² Score: {r2:.2f}")

    # ------------------------------------
    # 7. Visualisering
    # ------------------------------------
    plt.figure(figsize=(8,6))
    plt.scatter(y_test, y_pred, color='blue', edgecolor='k')
    plt.xlabel("Faktiske PM10")
    plt.ylabel("Predikerte PM10")
    plt.title("Faktiske vs. Predikerte PM10 verdier")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.show()

    # ------------------------------------
    # 8. Prediksjon for nye værforhold
    # ------------------------------------
    ny_data = pd.DataFrame({'avg_temp': [20], 'precipitation': [5], 'wind_speed': [3]})
    prediksjon = model.predict(ny_data)
    print(f"\nPredikert PM10 for 20°C, 5 mm nedbør, 3 m/s vind: {prediksjon[0]:.2f}")

else:
    print("\n⚠️ Ikke nok data til å trene modellen. Prøv å hente lengre periode.")

# ------------------------------------
# 9. Oppsummering
# ------------------------------------
print("\nOppsummering:")
print("- Modellen forsøker å forutsi PM10 basert på værforhold.")
print("- Kilder: Frost API (vær) + NILU historiske data (luftkvalitet).")
print("- Resultatet viser om det finnes sammenheng mellom vær og luftkvalitet.")
