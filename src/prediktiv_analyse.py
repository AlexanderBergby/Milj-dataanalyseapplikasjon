"""
prediktiv_analyse.py
Dette skriptet utfører en prediktiv analyse av temperaturdata ved hjelp av lineær regresjon.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tkinter as tk
import calendar
from tkinter import messagebox

def prediktiv():
    #Sier hvilken fildata som skal brukes
    data = "data/csv/renset_tempdata_Theim.csv"

    #Try/except på åpning av fil
    try:
        df = pd.read_csv(data, sep=";")
    except FileNotFoundError:
        messagebox.showerror("Feil", f"Filen '{data}' finnes ikke.")
        return

    #Dataprepparering i filen, konverterer dato til tall, forenklere kolonnenavn, erstatter NaN
    try:
        df["Date"] = pd.to_datetime(df["Date"])
        df["month"] = df["Date"].dt.month
        df.rename(columns={
            "Maksimumstemperatur (mnd)": "max_temp",
            "Minimumstemperatur (mnd)": "min_temp"
        }, inplace=True)
        df["max_temp_prev"] = df["max_temp"].shift(1)
        df["min_temp_prev"] = df["min_temp"].shift(1)
        df.dropna(inplace=True)
    except Exception as e:
        messagebox.showerror("Feil", f"Det oppstod en feil under databehandling: {e}")
        return

    #Definerer uavhengige variabler (X) og avhengig variabel (y)
    X = df[["month", "min_temp", "max_temp_prev", "min_temp_prev"]]
    y = df["max_temp"]

    #tilfeldig deling av datasett (train-test split)
    X_train, X_test, y_train, y_test, _, dato_test = train_test_split(
        X, y, df["Date"], test_size=0.2, random_state=0
    )

    #Modelltrening
    modell = LinearRegression()
    modell.fit(X_train, y_train)
    y_pred = modell.predict(X_test)

    #Beregning av MSE, RMSE og R²
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    #Prediksjon for neste måned
    siste = df.iloc[-1]
    neste_måned = (siste["month"] % 12) + 1
    X_neste = pd.DataFrame([{
        "month": neste_måned,
        "min_temp": siste["min_temp"],
        "max_temp_prev": siste["max_temp"],
        "min_temp_prev": siste["min_temp"]
    }])
    pred_neste = modell.predict(X_neste)[0]

    #GUI-visning for prediktiv analyse
    vindu = tk.Toplevel()
    vindu.title("Prediktiv temperatur for neste måned")
    vindu.geometry("400x250")
    vindu.resizable(False, False)

    #Viser månedsnavn for prediksjon
    måned_navn = calendar.month_name[int(neste_måned)]
    tekst = (
        "Resultater fra prediktiv analyse:\n\n"
        f" - RMSE: {rmse:.2f}\n"
        f" - R²-score: {r2:.2f}\n"
        f" - Neste måneds ({måned_navn}) predikerte maksimumstemperatur:\n"
        f"   {pred_neste:.2f} °C\n\n"
        "Merk: Resultatene vil forbedres\nmed mer variert og historisk data."
    )

    #Legger til tekst og knapper til vinduet
    tk.Label(vindu, text="Prediktiv analyse", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(vindu, text=tekst, font=("Helvetica", 11), justify="left").pack(pady=5)
    tk.Button(vindu, text="Lukk", command=vindu.destroy).pack(pady=15)

    #Sorterer testsettet etter dato for korrekt visning i grafen
    plot_df = pd.DataFrame({
        "dato": dato_test,
        "faktisk": y_test,
        "predikert": y_pred
    }).sort_values("dato")

    #Visualisering med matplotlib
    plt.figure(figsize=(8, 4))
    plt.plot(plot_df["dato"], plot_df["faktisk"].values, label="Faktisk")
    plt.plot(plot_df["dato"], plot_df["predikert"].values, label="Predikert", linestyle="--")
    plt.title("Faktisk vs. predikert maksimumstemperatur")
    plt.xlabel("År") 
    plt.ylabel("Temperatur(°C)") 
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    prediktiv()