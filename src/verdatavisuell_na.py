import requests
import json
import os
import tkinter as tk
from tkinter import messagebox

#API-innstillinger
url = "https://api.met.no/weatherapi/nowcast/2.0/complete"
headers = {"User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"}

#Henter værdata for én posisjon
def henter_vær_data(lat, lon):

    params = {"lat": lat, "lon": lon}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Feil", f"Feil under henting av data. Statuskode: {response.status_code}")
        return None

#Viser værvindu for valgt by
def lager_vær_vindu(by, data):
     #Henter den første målingen
    første = data["properties"]["timeseries"][0]
    time_text = første.get("time", "Ukjent tid")
    details = første.get("data", {}).get("instant", {}).get("details", {})
    air_temp = details.get("air_temperature", "N/A")
    precip_rate = details.get("precipitation_rate", "N/A")
    relative_humidity = details.get("relative_humidity", "N/A")
    wind_speed = details.get("wind_speed", "N/A")
    wind_gust = details.get("wind_speed_of_gust", "N/A")

    #Finner vær-symbolet for dem neste time
    symbol = første.get("data", {}).get("next_1_hours", {}).get("summary", {}).get("symbol_code", "")
    if "clearsky" in symbol:
        ikon = "☀️"
    elif "rain" in symbol:
        ikon = "🌧️"
    elif "cloud" in symbol or "partlycloudy" in symbol:
        ikon = "☁️"
    else:
        ikon = "❓"
    #Oppretter et Tkinter-vindu
    vindu = tk.Toplevel()
    vindu.title("Værmelding for " + by)
    vindu.geometry("400x350")

    #Lager etiketter for å vise værdataene
    tk.Label(vindu, text=f"Værmelding for: {by}", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(vindu, text=f"Tid: {time_text}", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=f"Lufttemperatur: {air_temp} °C", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=f"Nedbør: {precip_rate} mm/h", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=f"Luftfuktighet: {relative_humidity}%", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=f"Vind: {wind_speed} m/s", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=f"Vindkast: {wind_gust} m/s", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(vindu, text=ikon, font=("Helvetica", 48)).pack(pady=10)


#Hovedfunksjon for GUI-menyvalg
def værdata_nå_visuell(root):
    def hent_og_vis(lat, lon, by):
        lagre_temperaturdata()
        data = henter_vær_data(lat, lon)
        if data:
            lager_vær_vindu(by, data)

    #Nytt vindu med byvalg
    velger_vindu = tk.Toplevel(root)
    velger_vindu.title("Velg by")
    velger_vindu.geometry("300x320")
    velger_vindu.resizable(False, False)


    tk.Label(velger_vindu, text="Velg en by:", font=("Helvetica", 14, "bold")).pack(pady=15)


    byvalg = [
        ("Trondheim", 63.4308, 10.4034),
        ("Oslo", 59.9139, 10.7522),
        ("Bergen", 60.3913, 5.3221),
        ("Stavanger", 58.9690, 5.7331),
        ("Tromsø", 69.6496, 18.9560)
    ]

    for by, lat, lon in byvalg:
        tk.Button(
            velger_vindu,
            text=by,
            width=25,
            command=lambda b=by, la=lat, lo=lon: hent_og_vis(la, lo, b)
        ).pack(pady=5)

    def avslutt():
        velger_vindu.destroy()

    tk.Button(velger_vindu, text="Avslutt", width=25, bg="red", fg="black", command=avslutt).pack(pady=15)


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

#For testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  #skjuler hovedvinduet, men det trengs for å holde GUI i gang
    værdata_nå_visuell(root)
    root.mainloop()
    