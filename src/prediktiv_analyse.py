import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import tkinter as tk
import calendar
from tkinter import messagebox

def prediktiv():
    #Sier hvilken fildata som skal brukes
    data = "data/csv/renset_tempdata_Theim.csv"

    #try/except på åpning av fil
    try:
        df = pd.read_csv(data, sep=";")
    except FileNotFoundError:
        messagebox.showerror("Feil", f"Filen '{data}' finnes ikke.")
        return
    
    #Dataprepparering i filen, konverterer dato til tall, forenklere kolonnenavn, ertsatte NaN
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
    #Modelltrening
    X = df[["month", "min_temp", "max_temp_prev", "min_temp_prev"]]
    y = df["max_temp"]

    #Deler opp i trening og test-sett
    cutoff = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:cutoff], X.iloc[cutoff:]
    y_train, y_test = y.iloc[:cutoff], y.iloc[cutoff:]

    #Tren modell
    modell = LinearRegression()
    modell.fit(X_train, y_train)
    y_pred = modell.predict(X_test)

    #Mean Squared Error (MSE)
    #Root Mean Squared Error (RMSE)
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

    #GUI-visning
    vindu = tk.Toplevel()
    vindu.title("Prediktiv temperatur for neste måned")
    vindu.geometry("400x250")
    vindu.resizable(False, False)
    #for å vise måned som string og ikke int
    måned_navn = calendar.month_name[int(neste_måned)]
    tekst = (
        "Resultater fra prediktiv analyse:\n\n"
        f" - RMSE: {rmse:.2f}\n"
        f" - R²-score: {r2:.2f}\n"
        f" - Neste måneds ({måned_navn}) predikerte maksimumstemperatur:\n"
        f"   {pred_neste:.2f} °C\n\n"
        "Merk: Resultatene vil forbedres\nmed mer variert og historisk data."
    )

    tk.Label(vindu, text="Prediktiv analyse", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(vindu, text=tekst, font=("Helvetica", 11), justify="left").pack(pady=5)
    tk.Button(vindu, text="Lukk", command=vindu.destroy).pack(pady=15)

    #Mer visualisering
    datoer = df["Date"].iloc[cutoff:] 

    plt.figure(figsize=(8, 4))
    plt.plot(datoer, y_test.values, label="Faktisk")
    plt.plot(datoer, y_pred, label="Predikert", linestyle="--")
    plt.title("Faktisk vs. predikert maksimumstemperatur")
    plt.xlabel("Måned")
    plt.ylabel("Temperatur (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()