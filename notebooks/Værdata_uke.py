import requests
import numpy as np
from datetime import datetime, timedelta #for å kunne enklere behandle og visualisere dato og tid
import pandas as pd  #for å kunne lagre til CSV til sendere databehandling
import numpy as np  #for å regne ut median og standardavvik
import matplotlib.pyplot as plt
import seaborn as sns
import os

#sjekker at data-mappen finnes
if not os.path.exists("data"):
    os.makedirs("data")

#API-passord osv
client_id = "e1e74478-764e-4bac-8a69-f70fe2ed8c6d"  # API-nøkkel
observations_url = "https://frost.met.no/observations/v0.jsonld"  # URL til værdata

valgt_stasjon = "SN68090"
print("\nVærstasjon: Trondheim - Granåsen.")

#Elementene vi ønsker å hente fra API-et
temperatur_element = "air_temperature"
nedbør_element = "sum(precipitation_amount P1D)"
vindhastighet_element = "wind_speed"

#Beregn datoer for de siste 7 dagene
idag = datetime.utcnow().date()  #Dagens dato i UTC
start_dato = (idag - timedelta(days=7)).strftime("%Y-%m-%d")  #Startdato
slutt_dato = idag.strftime("%Y-%m-%d")  #Sluttdato 

#Parametere for API
params = {
    "sources": valgt_stasjon,
    "elements": f"{temperatur_element},{nedbør_element},{vindhastighet_element}",
    "referencetime": f"{start_dato}/{slutt_dato}"
}

response = requests.get(observations_url, params=params, auth=(client_id, ""))

if response.status_code == 200:  #Sjekker om forespørselen var vellykket
    data = response.json()["data"]

    #lagrer data
    temperatur_data = {}
    nedbør_data = {}
    vind_data = {}

    for entry in data:
        dato = entry["referenceTime"][:10]
        observasjoner = entry["observations"]

        for obs in observasjoner:
            verdi = obs["value"]
            element = obs["elementId"]

            if element == temperatur_element:
                temperatur_data.setdefault(dato, []).append(verdi)
            if element == nedbør_element:
                nedbør_data[dato] = nedbør_data.get(dato, 0) + verdi  #Summerer nedbør
            if element == vindhastighet_element:
                vind_data.setdefault(dato, []).append(verdi)

    print("\nVærforhold de siste 7 dagene\n")
    rows = []  #Samler data til CSV

    #Beregn statistikk for hver dag
    for dag_nummer, dato in enumerate(sorted(temperatur_data.keys()), 1):
        min_temp = min(temperatur_data[dato])
        max_temp = max(temperatur_data[dato])
        gjennomsnitt_temp = round(sum(temperatur_data[dato]) / len(temperatur_data[dato]), 2)
        median_temp = round(np.median(temperatur_data[dato]), 2)
        std_temp = round(np.std(temperatur_data[dato]), 2)
        nedbør_mengde = nedbør_data.get(dato, 0)
        vindhastighet = (
            round(sum(vind_data[dato]) / len(vind_data[dato]), 2)
            if dato in vind_data and vind_data[dato]
            else None  #Bruker None hvis ingen data finnes
        )
        
        print(f"Dag {dag_nummer}: {dato}")
        print(f"   Temperatur: Snitt {gjennomsnitt_temp:.1f}°C, Median {median_temp:.1f}°C, Std {std_temp:.1f}°C (Min: {min_temp}°C, Max: {max_temp}°C)")
        print(f"   Nedbør: {nedbør_mengde:.1f} mm")
        print(f"   Vindhastighet: {vindhastighet if vindhastighet is not None else 'N/A'} m/s\n")
        
        #Legger alle verdiene i en ordbok for hver dag
        rows.append({
            "date": dato,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": gjennomsnitt_temp,
            "median_temp": median_temp,
            "std_temp": std_temp,
            "precipitation": nedbør_mengde,
            "wind_speed": vindhastighet
        })
    
    #Lager DataFrame og lagrer til CSV
    df = pd.DataFrame(rows)
    filnavn = "data/weather_data.csv"
    df.to_csv(filnavn, index=False)
    print(f"Data lagret i mappen 'data' som '{filnavn}'.")
else:
    print("\nFeil ved henting av værdata:", response.status_code, response.text)
