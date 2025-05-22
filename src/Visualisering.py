import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Setter Seaborn-tema
sns.set_theme(style="darkgrid", context="talk")

def visualisering():
    filnavn = 'data/csv/weather_data.csv'

    #Leser CSV-filen inn i en DataFrame og konverter 'date'-kolonnen til datetime
    try:
        df = pd.read_csv(filnavn, parse_dates=['date'])
    except FileNotFoundError:
        print(f"Filen '{filnavn}' ble ikke funnet. Sørg for at du har kjørt alternativ 2 i menyen først.")
        return

    df.set_index('date', inplace=True)
    # Fyller området mellom min_temp og max_temp
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.fill_between(df.index, df['min_temp'], df['max_temp'],
                     color='gray', alpha=0.3, label='Min/Max område')
    # Plotter gjennomsnittstemperaturen med error bars basert på standardavvik
    ax1.errorbar(df.index, df['avg_temp'], yerr=df['std_temp'],
                 fmt='o-', capsize=5, label='Gj.snitt Temp ± Std')
    # Plotter mediantemperaturen
    sns.lineplot(x=df.index, y=df['median_temp'], marker="s", ax=ax1,
                 label='Median Temp', linewidth=3)

    ax1.set_title('Temperaturutvikling med statistikk')
    ax1.set_xlabel('Dato')
    ax1.set_ylabel('Temperatur (°C)')
    ax1.legend()
    plt.setp(ax1.get_xticklabels(), rotation=25)
    plt.show()


#For testing
if __name__ == "__main__":
    visualisering()
