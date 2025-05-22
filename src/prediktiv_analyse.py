import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import tkinter as tk
from tkinter import messagebox


def prediktiv():
    #Sier hvilken data som skal brukes
    data = "data/csv/weather_data.csv"

    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        messagebox.showerror("Feil", f"Filen '{data}' finnes ikke.\nKjør alternativ 2 først for å hente værdata.")
        return
    
    # Sjekk at nødvendige kolonner finnes
    if not {'wind_speed', 'precipitation', 'avg_temp'}.issubset(df.columns):
        messagebox.showerror("Feil", "Datasettet mangler nødvendige kolonner for prediktiv analyse.")
        return
    #Predikere gjennomsnittstemperatur basert på vindhastighet og nedbør
    #Resultatene er dårlige nå, men vil forhåpentligvis bli bedre med mer data
    X = df[['wind_speed', 'precipitation']]
    y = df['avg_temp']
    
    #Deler data inn i trenings- og testsett
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    #Trener modellen
    modell = LinearRegression()
    modell.fit(X_train, y_train)
    
    #Gjør prediksjoner
    y_pred = modell.predict(X_test)

    #Mean Squared Error (MSE)
    #Root Mean Squared Error (RMSE)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    #GUI-visning
    vindu = tk.Toplevel()
    vindu.title("Prediktiv analyse")
    vindu.geometry("400x250")
    vindu.resizable(False, False)

    tekst = (
        "Resultater fra prediktiv analyse:\n\n"
        f" - RMSE: {rmse:.2f}\n"
        f" - R²-score: {r2:.2f}\n\n"
        "Merk: Resultatene vil forbedres\nmed mer variert og historisk data."
    )

    tk.Label(vindu, text="Prediktiv analyse", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(vindu, text=tekst, font=("Helvetica", 11), justify="left").pack(pady=5)
    tk.Button(vindu, text="Lukk", command=vindu.destroy).pack(pady=15)
