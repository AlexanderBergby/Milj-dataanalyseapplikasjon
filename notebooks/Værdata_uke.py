import requests
from datetime import datetime, timedelta #for å kunne enklere behandle og visualisere dato og tid
import pandas as pd  #for å kunne lagre til CSV til sendere databehandling

client_id = "e1e74478-764e-4bac-8a69-f70fe2ed8c6d" # API-nøkkel
observations_url = "https://frost.met.no/observations/v0.jsonld" # URL til værdata


valgt_stasjon = "SN68090" # Værstasjon ID
print("\nVærstasjon: Trondheim - Granåsen.")

#Elementene vi ønsker å hente fra API-en
temperatur_element = "air_temperature"
nedbør_element = "sum(precipitation_amount P1D)"
vindhastighet_element = "wind_speed"

#Henter data for de siste 7 dagene ved hjelp av datetime som er importert
idag = datetime.utcnow().date() #henter dagens dato i UTC
start_dato = (idag - timedelta(days=7)).strftime("%Y-%m-%d") #trekker fra 7 dager i fra dagens dato og lagrer som start-dato som string
slutt_dato = idag.strftime("%Y-%m-%d") #lagrer sluttdato som string

# Parametere for API-forespørsel
params = {
    "sources": valgt_stasjon,
    "elements": f"{temperatur_element},{nedbør_element},{vindhastighet_element}",
    "referencetime": f"{start_dato}/{slutt_dato}"
}

response = requests.get(observations_url, params=params, auth=(client_id, "")) #gjennomfører API-kallet

if response.status_code == 200: #200 betyr at alt fungerte i request
    data = response.json()["data"]

    # Lagring av data
    temperatur_data = {}
    nedbør_data = {}
    vind_data = {}

    for entry in data:
        dato = entry["referenceTime"][:10]  # YYYY-MM-DD
        observasjoner = entry["observations"]

        for obs in observasjoner:
            verdi = obs["value"]
            element = obs["elementId"]
            #lagrer data for de ulike tidpsunktene i en liste
            if element == temperatur_element:
                temperatur_data.setdefault(dato, []).append(verdi)

            if element == nedbør_element:
                nedbør_data[dato] = nedbør_data.get(dato, 0) + verdi  # Summer nedbør

            if element == vindhastighet_element:
                vind_data.setdefault(dato, []).append(verdi)

    # Skriver ut sammendrag til terminal
    print("\nVærforhold de siste 7 dagene\n")
    rows = []  # Samler data til senere bruk i CSV

    #finner min og max og gjennomsnitt for hver dag i listen av temperaturer 
    for dag_nummer, dato in enumerate(sorted(temperatur_data.keys()), 1):
        min_temp = min(temperatur_data[dato])
        max_temp = max(temperatur_data[dato])
        gjennomsnitt_temp = sum(temperatur_data[dato]) / len(temperatur_data[dato])

        nedbør_mengde = nedbør_data.get(dato, 0)

        vindhastighet = (
            sum(vind_data[dato]) / len(vind_data[dato])
            if dato in vind_data and vind_data[dato]
            else None  # Bruk None i stedet for "N/A"
        )

        print(f"Dag {dag_nummer}: {dato}")
        print(f"   Temperatur: Snitt {gjennomsnitt_temp:.1f}°C (Min: {min_temp}°C, Max: {max_temp}°C)")
        print(f"   Nedbør: {nedbør_mengde:.1f} mm")
        print(f"   Vindhastighet: {vindhastighet if vindhastighet is not None else 'N/A'} m/s\n")

        #Her samler vi alt i en liste med dictionaries som senere blir til en DataFrame.
        rows.append({
            "date": dato,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": gjennomsnitt_temp,
            "precipitation": nedbør_mengde,
            "wind_speed": vindhastighet
        })

    # Opprett en DataFrame for å lagre til CSV
    df = pd.DataFrame(rows)
    df.to_csv("data/weather_data.csv", index=False)

    print("Data lagret i folderen Data som 'weather_data.csv'.")

else:
    print("\nFeil ved henting av værdata:", response.status_code, response.text)
