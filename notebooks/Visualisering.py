import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Seaborn Tema
sns.set_theme(style="darkgrid", context="talk")


filnavn = 'data/weather_data.csv'

# Leser CSV-filen inn i en DataFrame og konverter 'date'-kolonnen til datetime
df = pd.read_csv(filnavn, parse_dates=['date'])
df.set_index('date', inplace=True)

# Opprett figur og akse
fig, ax = plt.subplots(figsize=(12, 6))

# Fyll området mellom min_temp og max_temp
ax.fill_between(df.index, df['min_temp'], df['max_temp'],
                color='gray', alpha=0.3, label='Min/Max område')

# Plot gjennomsnittstemperaturen
sns.lineplot(x=df.index, y=df['avg_temp'], marker="o", ax=ax,
             label='Gj.snitt Temp', linewidth=3)

ax.set_title('Temperaturutvikling')
ax.set_xlabel('Dato')
ax.set_ylabel('Temperatur (°C)')
ax.legend()
plt.xticks(rotation=25)
plt.show()
