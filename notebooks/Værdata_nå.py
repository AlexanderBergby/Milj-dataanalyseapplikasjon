import requests

url = "https://api.met.no/weatherapi/nowcast/2.0/complete"

def meny():
    print("Velkommen til værappen!")
    print("1. Sjekk været i Trondheim")
    print("2. Sjekk været i Oslo")
    print("3. Sjekk været i Bergen")
    print("4. Avslutt")

    while True:
        valg = input("Velg et alternativ: ")
        if valg == "1":
            lat = 63.4308
            lon = 10.4034
            by = "Trondheim"
            break
        
        if valg == "2":
            lat = 59.9139
            lon = 10.7522
            by = "Oslo"
            break

        if valg == "3":
            lat = 60.3913
            lon = 5.3221
            by = "Bergen"
            break

        if valg == "4":
            print("Ha en fin dag!")
            return None, None
        else:
            print("Ugyldig valg. Prøv igjen.")

    return lat, lon, by

lat, lon, by = meny()
if lat is None or lon is None:
    exit()

params = {
    "lat": lat,   # Latitude
    "lon": lon    # Longitude
}

headers = {
    "User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"
}

# Send en GET-forespørsel til API-et
response = requests.get(url, params=params, headers=headers)

# Sjekk om responsen var vellykket
if response.status_code == 200:
    data = response.json() # Konverter JSON til et Python-objekt
    
    # Skriv ut den første målingen
    første = data["properties"]["timeseries"][0]
    print("-" * 40)
    print("Værdata for:", by)
    print("Tid:", første.get("time", "Ukjent tid")) # Hent ut tidspunktet for målingen, eller "Ukjent tid" hvis det ikke finnes
    detaljer = første.get("data", {}).get("instant", {}).get("details", {}) # Hent ut detaljene for målingen
    print("Lufttemperatur:", detaljer.get("air_temperature", "N/A"), "°C") # Hent ut lufttemperatur, eller "N/A" hvis det ikke finnes
    print("Nedbørsmengde per time:", detaljer.get("precipitation_rate", "N/A"), "mm/h") # Hent ut nedbørsmengde per time, eller "N/A" hvis det ikke finnes
    print("Relativ luftfuktighet:", detaljer.get("relative_humidity", "N/A"), "%") # Hent ut relativ luftfuktighet, eller "N/A" hvis det ikke finnes
    print("Vindhastighet:", detaljer.get("wind_speed", "N/A"), "m/s") # Hent ut vindhastighet, eller "N/A" hvis det ikke finnes
    print("Vindkast:", detaljer.get("wind_speed_of_gust", "N/A"), "m/s") # Hent ut vindkast, eller "N/A" hvis det ikke finnes
    
    
    # Sjekk de resterende målingene for nedbør
    regn_check = False 
    for entry in data["properties"]["timeseries"][1:]: #Itererer over de resterende målingene
        detaljer_entry = entry.get("data", {}).get("instant", {}).get("details", {})
        if detaljer_entry.get("precipitation_rate", 0) != 0: # Sjekker om det er nedbør
            regn_check = True
            break
        
    if regn_check:
        print("Det kommer til å bli regn de neste 2 timene.")
        print("-" * 40)
    else:
        print("Det skal ikke bli noe regn de neste 2 timene.")
        print("-" * 40)
else:
    print("Feil under henting av data. Statuskode:", response.status_code)
