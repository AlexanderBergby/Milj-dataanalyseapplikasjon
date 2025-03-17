# ------------------------------------
# 1. Importer nødvendige biblioteker
# ------------------------------------
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Sett Seaborn-tema
sns.set_theme(style="darkgrid", context="talk")
filnavn = 'data/weather_data.csv'  # Sørg for at filen ligger i riktig mappe

# Les CSV-filen inn i en DataFrame og konverter 'date'-kolonnen til datetime
df = pd.read_csv(filnavn, parse_dates=['date'])
df.set_index('date', inplace=True)

# Opprett figur og akse
fig, ax = plt.subplots(figsize=(12, 6))

# Fyll området mellom min_temp og max_temp
ax.fill_between(df.index, df['min_temp'], df['max_temp'],
                color='gray', alpha=0.3, label='Min/Max område')

# Plot gjennomsnittstemperaturen med error bars for standardavvik
ax.errorbar(df.index, df['avg_temp'], yerr=df['std_temp'],
            fmt='o-', capsize=5, label='Gj.snitt Temp ± Std')

# ------------------------------------
# 4. Slå sammen data
# ------------------------------------
print("\nSlår sammen vær- og luftkvalitetsdata...")

combined_df = pd.merge(weather_df, df_pivot, on='date', how='inner')
print("\nSammenslått datasett:\n", combined_df.head())

# ------------------------------------
# 5. Tren lineær regresjonsmodell (forutsi PM10)
# ------------------------------------
print("\nTrener prediktiv modell for PM10...")

X = combined_df[['avg_temp', 'precipitation', 'wind_speed']].fillna(0)  # Features
y = combined_df['PM10']  # Target

# Kun hvis vi har nok data
if len(combined_df) > 5:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # ------------------------------------
    # 6. Evaluer modellen
    # ------------------------------------
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nModell-evaluering:\nMean Squared Error (MSE): {mse:.2f}\nR² Score: {r2:.2f}")

    # ------------------------------------
    # 7. Visualisering
    # ------------------------------------
    plt.figure(figsize=(8,6))
    plt.scatter(y_test, y_pred, color='blue', edgecolor='k')
    plt.xlabel("Faktiske PM10")
    plt.ylabel("Predikerte PM10")
    plt.title("Faktiske vs. Predikerte PM10 verdier")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.show()

    # ------------------------------------
    # 8. Prediksjon for nye værforhold
    # ------------------------------------
    ny_data = pd.DataFrame({'avg_temp': [20], 'precipitation': [5], 'wind_speed': [3]})
    prediksjon = model.predict(ny_data)
    print(f"\nPredikert PM10 for 20°C, 5 mm nedbør, 3 m/s vind: {prediksjon[0]:.2f}")

else:
    print("\n⚠️ Ikke nok data til å trene modellen. Prøv å hente lengre periode.")

# ------------------------------------
# 9. Oppsummering
# ------------------------------------
print("\nOppsummering:")
print("- Modellen forsøker å forutsi PM10 basert på værforhold.")
print("- Kilder: Frost API (vær) + NILU historiske data (luftkvalitet).")
print("- Resultatet viser om det finnes sammenheng mellom vær og luftkvalitet.")
