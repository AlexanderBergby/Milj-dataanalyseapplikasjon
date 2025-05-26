"""
uteliggere.py
Dette skriptet identifiserer og viser uteliggere i maksimumstemperaturdata fra en CSV-fil.
"""

import pandas as pd

#Laster inn datafilen
df = pd.read_csv("data/csv/renset_tempdata_Theim.csv", sep=";")

#Gjør kolonnenavnet lettere å bruke
df.rename(columns={"Maksimumstemperatur (mnd)": "max_temp"}, inplace=True)

#Beregner IQR (interkvartilavstand)
Q1 = df["max_temp"].quantile(0.25)
Q3 = df["max_temp"].quantile(0.75)
IQR = Q3 - Q1

#Definer uteliggergrenser
nedre_grense = Q1 - 1.5 * IQR
øvre_grense = Q3 + 1.5 * IQR

#Filtrer ut uteliggere
outliers = df[(df["max_temp"] < nedre_grense) | (df["max_temp"] > øvre_grense)]

#Vis resultatet
print("Uteliggere i maksimumstemperatur:")
print(outliers[["Date", "max_temp"]])


