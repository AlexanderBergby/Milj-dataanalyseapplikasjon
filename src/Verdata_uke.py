import requests
import numpy as np
from datetime import datetime, timedelta, UTC
import pandas as pd
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

def værdata_uke():
    #sjekker at data-mappen finnes
    if not os.path.exists("data"):
        os.makedirs("data")
    
    #API-passord osv
    client_id = "e1e74478-764e-4bac-8a69-f70fe2ed8c6d"
    observations_url = "https://frost.met.no/observations/v0.jsonld"
    valgt_stasjon = "SN68090"  # Trondheim – Granåsen
    
    #Elementene vi ønsker å hente fra API-et
    temperatur_element = "air_temperature"
    nedbør_element = "sum(precipitation_amount P1D)"
    vindhastighet_element = "wind_speed"

    #Beregn datoer for de siste 7 dagene
    idag = datetime.now(UTC).date()
    start_dato = (idag - timedelta(days=7)).strftime("%Y-%m-%d")
    slutt_dato = idag.strftime("%Y-%m-%d")

    #Parametere for API
    params = {
        "sources": valgt_stasjon,
        "elements": f"{temperatur_element},{nedbør_element},{vindhastighet_element}",
        "referencetime": f"{start_dato}/{slutt_dato}"
    }

    response = requests.get(observations_url, params=params, auth=(client_id, ""))

    if response.status_code != 200:
        messagebox.showerror("Feil", f"Feil ved henting av værdata:\n{response.status_code}")
        return

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
                nedbør_data[dato] = nedbør_data.get(dato, 0) + verdi
            if element == vindhastighet_element:
                vind_data.setdefault(dato, []).append(verdi)

    rows = []  #Samler data til CSV
    output_text = "Værforhold - Trondheim (Granåsen)\n\n"

    #Beregner statistikk for hver dag
    for dag_nummer, dato in enumerate(sorted(temperatur_data.keys()), 1):
        min_temp = min(temperatur_data[dato])
        max_temp = max(temperatur_data[dato])
        avg_temp = round(sum(temperatur_data[dato]) / len(temperatur_data[dato]), 2)
        median_temp = round(np.median(temperatur_data[dato]), 2)
        std_temp = round(np.std(temperatur_data[dato]), 2)
        nedbør = nedbør_data.get(dato, 0)
        vind = (
            round(sum(vind_data[dato]) / len(vind_data[dato]), 2)
            if dato in vind_data and vind_data[dato] else None
        )

        output_text += (
            f"Dag {dag_nummer}: {dato}\n"
            f"  Temperatur: Snitt {avg_temp:.1f}°C, Median {median_temp:.1f}°C, Std {std_temp:.1f}°C "
            f"(Min: {min_temp}°C, Max: {max_temp}°C)\n"
            f"  Nedbør: {nedbør:.1f} mm\n"
            f"  Vindhastighet: {vind if vind is not None else 'N/A'} m/s\n\n"
        )
        #Legger alle verdiene i en ordbok for hver dag
        rows.append({
            "date": dato,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp,
            "median_temp": median_temp,
            "std_temp": std_temp,
            "precipitation": nedbør,
            "wind_speed": vind
        })

    #Lager DataFrame og lagrer til CSV
    df = pd.DataFrame(rows)
    filnavn = "data/csv/weather_data.csv"
    df.to_csv(filnavn, index=False)

    #GUI-visning
    vindu = tk.Toplevel()
    vindu.title("Værdata – siste uke")

    vindu.geometry("400x400")

    tk.Label(vindu, text="Værdata for Trondheim (Granåsen)", font=("Helvetica", 14, "bold")).pack(pady=10)

    tekstboks = scrolledtext.ScrolledText(vindu, wrap=tk.WORD, font=("Courier", 10), width=70, height=20)
    tekstboks.insert(tk.END, output_text)
    tekstboks.configure(state="disabled")
    tekstboks.pack(padx=10, pady=10)

    tk.Button(vindu, text="Lukk", command=vindu.destroy).pack(pady=10)

#For testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    værdata_uke()
    root.mainloop()
