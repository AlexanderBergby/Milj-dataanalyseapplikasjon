import requests
import tkinter as tk
from tkinter import messagebox

#Henter API og setter parametere
def get_weather_data(lat, lon):
    url = "https://api.met.no/weatherapi/nowcast/2.0/complete"
    params = {"lat": lat, "lon": lon}
    headers = {"User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Feil", f"Feil under henting av data. Statuskode: {response.status_code}")
        return None

def create_weather_window(by, data):
    #Henter den første målingen
    første = data["properties"]["timeseries"][0]
    time_text = første.get("time", "Ukjent tid")
    details = første.get("data", {}).get("instant", {}).get("details", {})
    air_temp = details.get("air_temperature", "N/A")
    precip_rate = details.get("precipitation_rate", "N/A")
    relative_humidity = details.get("relative_humidity", "N/A")
    wind_speed = details.get("wind_speed", "N/A")
    wind_gust = details.get("wind_speed_of_gust", "N/A")
    #Finner vær-symbolet for den neste time
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
    root = tk.Tk()
    root.title("Værmelding for " + by)
    root.geometry("400x350")

    #Lager etiketter for å vise værdataene
    tk.Label(root, text="Værmelding for: " + by, font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(root, text="Tid: " + time_text, font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Lufttemperatur: {air_temp} °C", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Nedbør per time: {precip_rate} mm/h", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Relativ luftfuktighet: {relative_humidity}%", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Vindhastighet: {wind_speed} m/s", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=f"Vindkast: {wind_gust} m/s", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text=ikon, font=("Helvetica", 48)).pack(pady=10)
    
    root.mainloop()

#Meny for valg av by
def værdata_nå_visuell():
    print("1. Trondheim\n2. Oslo\n3. Bergen\n4. Avslutt")
    while True:
        valg = input("Velg et alternativ: ")
        if valg == "1":
            lat, lon, by = 63.4308, 10.4034, "Trondheim"
            break
        elif valg == "2":
            lat, lon, by = 59.9139, 10.7522, "Oslo"
            break
        elif valg == "3":
            lat, lon, by = 60.3913, 5.3221, "Bergen"
            break
        elif valg == "4":
            print("Ha en fin dag!")
            return
        else:
            print("Ugyldig valg. Prøv igjen.")
    
    data = get_weather_data(lat, lon)
    if data:
        create_weather_window(by, data)

#For testing
if __name__ == "__main__":
    værdata_nå_visuell()
