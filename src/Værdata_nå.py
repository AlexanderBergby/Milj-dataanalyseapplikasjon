import requests
import json
import os

url = "https://api.met.no/weatherapi/nowcast/2.0/complete"
headers = {
    "User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"
}

def meny():
    print("Velkommen til værappen!")
    print("1. Sjekk været i Trondheim")
    print("2. Sjekk været i Oslo")
    print("3. Sjekk været i Bergen")
    print("4. Sjekk været i Stavanger")
    print("5. Sjekk været i Tromsø")
    print("6. Avslutt")

    while True:
        valg = input("Velg et alternativ: ")
        if valg == "1":
            lat = 63.4308
            lon = 10.4034
            by = "Trondheim"
            break
        elif valg == "2":
            lat = 59.9139
            lon = 10.7522
            by = "Oslo"
            break
        elif valg == "3":
            lat = 60.3913
            lon = 5.3221
            by = "Bergen"
            break
        elif valg == "4":
            lat = 58.9690
            lon = 5.7331
            by = "Stavanger"
            break
        elif valg == "5":
            lat = 69.6496
            lon = 18.9560
            by = "Tromsø"
            break
        elif valg == "6":
            print("Ha en fin dag!")
            return None, None, None
        else:
            print("Ugyldig valg. Prøv igjen.")

    return lat, lon, by


def lagre_temperaturdata(filbane="data/temperaturdata.json"):
    byer = {
        "Oslo": (59.9139, 10.7522),
        "Bergen": (60.3913, 5.3221),
        "Trondheim": (63.4308, 10.4034),
        "Stavanger": (58.9690, 5.7331),
        "Tromsø": (69.6496, 18.9560)
    }

    resultat = []

    for by_navn, (lat, lon) in byer.items():
        params = {"lat": lat, "lon": lon}
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            detaljer = data["properties"]["timeseries"][0]["data"]["instant"]["details"]
            temperatur = detaljer.get("air_temperature", None)
            if temperatur is not None:
                resultat.append({
                    "city": by_navn,
                    "temperature": temperatur
                })
            else:
                print(f"Ingen temperaturdata for {by_navn}")
        else:
            print(f"Feil ved henting av data for {by_navn}: {response.status_code}")

    os.makedirs(os.path.dirname(filbane), exist_ok=True)

    with open(filbane, "w") as f:
        json.dump(resultat, f)

    print(f"Temperaturdata lagret i: {filbane}")


if __name__ == "__main__":
    lat, lon, by = meny()
    if lat is None or lon is None:
        exit()

    params = {"lat": lat, "lon": lon}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        første = data["properties"]["timeseries"][0]
        print("-" * 40)
        print("Værdata for:", by)
        print("Tid:", første.get("time", "Ukjent tid"))
        detaljer = første.get("data", {}).get("instant", {}).get("details", {})
        print("Lufttemperatur:", detaljer.get("air_temperature", "N/A"), "°C")
        print("Nedbørsmengde per time:", detaljer.get("precipitation_rate", "N/A"), "mm/h")
        print("Relativ luftfuktighet:", detaljer.get("relative_humidity", "N/A"), "%")
        print("Vindhastighet:", detaljer.get("wind_speed", "N/A"), "m/s")
        print("Vindkast:", detaljer.get("wind_speed_of_gust", "N/A"), "m/s")

        regn_check = False 
        for entry in data["properties"]["timeseries"][1:]:
            detaljer_entry = entry.get("data", {}).get("instant", {}).get("details", {})
            if detaljer_entry.get("precipitation_rate", 0) != 0:
                regn_check = True
                break
            
        if regn_check:
            print("Det kommer til å bli regn de neste 2 timene.")
        else:
            print("Det skal ikke bli noe regn de neste 2 timene.")
        print("-" * 40)
    else:
        print("Feil under henting av data. Statuskode:", response.status_code)

    lagre_temperaturdata()
