import requests
from datetime import datetime, timedelta  # For å behandle dato og tid
import pandas as pd  # For å lagre og lese CSV
import numpy as np  # For å regne ut median og standardavvik
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Setter Seaborn-tema
sns.set_theme(style="darkgrid", context="talk")


filnavn = 'data/weather_data.csv'

#Leser CSV-filen inn i en DataFrame og konverter 'date'-kolonnen til datetime
df = pd.read_csv(filnavn, parse_dates=['date'])
df.set_index('date', inplace=True)

#Oppretter figur og akse
fig, ax = plt.subplots(figsize=(12, 6))

#Fyller området mellom min_temp og max_temp
ax.fill_between(df.index, df['min_temp'], df['max_temp'],
                color='gray', alpha=0.3, label='Min/Max område')

#Plotter gjennomsnittstemperaturen med error for standardavvik
ax.errorbar(df.index, df['avg_temp'], yerr=df['std_temp'],
            fmt='o-', capsize=5, label='Gj.snitt Temp ± Std')

#Plotter mediantemp som en egen linje
sns.lineplot(x=df.index, y=df['median_temp'], marker="s", ax=ax,
             label='Median Temp', linewidth=3)

ax.set_title('Temperaturutvikling med statistikk')
ax.set_xlabel('Dato')
ax.set_ylabel('Temperatur (°C)')
ax.legend()
plt.xticks(rotation=25)
plt.show()