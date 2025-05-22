import requests
import json
import os

#API
url = "https://api.met.no/weatherapi/nowcast/2.0/complete"
headers = {
    "User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"
}

#Meny for valg av by
def velg_by():
    print("1. Trondheim")
    print("2. Oslo")
    print("3. Bergen")
    print("4. Stavanger")
    print("5. Tromsø")
    print("6. Avslutt")

    while True:
        valg = input("Velg et alternativ: ")
        if valg == "1":
            return 63.4308, 10.4034, "Trondheim"
        elif valg == "2":
            return 59.9139, 10.7522, "Oslo"
        elif valg == "3":
            return 60.3913, 5.3221, "Bergen"
        elif valg == "4":
            return 58.9690, 5.7331, "Stavanger"
        elif valg == "5":
            return 69.6496, 18.9560, "Tromsø"
        elif valg == "6":
            print("Ha en fin dag!")
            return None, None, None
        else:
            print("Ugyldig valg. Prøv igjen.")

def lagre_temperaturdata(filbane="data/json/temperaturdata.json"):
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

def værdata_nå():
    lat, lon, by = velg_by()
    if lat is None or lon is None:
        return

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

        regn_check = any(
            entry.get("data", {}).get("instant", {}).get("details", {}).get("precipitation_rate", 0) != 0
            for entry in data["properties"]["timeseries"][1:3]
        )

        if regn_check:
            print("Det kommer til å bli regn de neste 2 timene.")
        else:
            print("Det skal ikke bli noe regn de neste 2 timene.")
        print("-" * 40)
    else:
        print("Feil under henting av data. Statuskode:", response.status_code)

    lagre_temperaturdata()

#For testing
if __name__ == "__main__":
    værdata_nå()
