""""
rensing.py
Dette skriptet renser temperaturdata fra en CSV-fil, konverterer data til riktig format,
interpolerer manglende verdier, og lagrer de rensede dataene i en ny CSV-fil.
"""

import pandas as pd
import numpy as np

# Leser data fra CSV-fil, som er lagret i UTF-8, og med semikolon som separator, holder kolonnen 'Tid(norsk normaltid)' som str
def rens_tempdata(fil_inn, fil_ut):
    df = pd.read_csv(fil_inn,
        sep=';',
        encoding='utf-8-sig',
        dtype={'Tid(norsk normaltid)': str}
    )

    # Renser data, endrer ',' til '.' (Må gjøre for å bruke pandas) og '-' til NaN, og konverterer til float
    for kol in ['Maksimumstemperatur (mnd)', 'Minimumstemperatur (mnd)']:
        rådata = df[kol].astype(str) 
        # Bytt ut '-' med np.nan
        df[kol] = rådata.replace('-', np.nan)

         #Bytt ut komma med punktum
        df[kol] = df[kol].str.replace(',', '.', regex=False)

        # Konverter til flyttall (float)
        df[kol] = df[kol].astype(float)

    # Leser ikke siste rad i dataene (Tillegsrad fra Meteorologisk institutt)
    df = df.iloc[:-1]   
    
    # Legger til en ny kolonne 'Date' som konverterer 'Tid(norsk normaltid)' til datetime-format, brukes i prediktiv analyse
    df['Date'] = pd.to_datetime(
    df['Tid(norsk normaltid)'],
    format='%m.%Y',   
    errors='raise'
)
    # Kun for å illustrere at det er NaN i dataene, og sjekker at rensingen er gjort riktig, har ingen funksjon utenom å visualisere.
    # Hvis det er NaN i første eller siste rad, så kan det ikke interpoleres, men pandas vil da bare sette NaN i stedet for å gi feil.
    for index in range(len(df)):
        min_value = df['Minimumstemperatur (mnd)'][index]
        max_value = df['Maksimumstemperatur (mnd)'][index]

        # Sjekker om det er NaN i dataene
        if pd.isna(min_value):
            print("Feil i rad nr: ", index + 2) # +2 fordi første rad er header, og pandas starter på 0
            print("Minimumstemperatur (mnd):", min_value)

            # Sjekker at det eksister forrige og neste rad og printer ut verdiene
            if index > 0 and index < len(df) - 1:
                interpolert_verdi = (df['Minimumstemperatur (mnd)'][index - 1] + df['Minimumstemperatur (mnd)'][index + 1]) / 2
                print("Forrige rad verdi:")
                print("  Minimumstemperatur (mnd):", df['Minimumstemperatur (mnd)'][index - 1])
                print("\n")
                print("Neste rad verdi:")
                print("  Minimumstemperatur (mnd):", df['Minimumstemperatur (mnd)'][index + 1])
                print("Den nye verdien blir: ", interpolert_verdi)
            else:
                print("Ingen forrige eller neste rad å hente verdi fra")


            print("-" * 40)

        if pd.isna(max_value):
            print("Feil i rad nr: ", index + 2) # +2 fordi første rad er header, og pandas starter på 0
            print("Maksimumstemperaturen (mnd):", min_value)

            # Sjekker at det eksister forrige og neste rad og printer ut verdiene
            if index > 0 and index < len(df) - 1:
                print("Maksimumstemperatur (mnd):", max_value)
                interpolert_verdi = (df['Maksimumstemperatur (mnd)'][index - 1] + df['Maksimumstemperatur (mnd)'][index + 1]) / 2
                print("Forrige rad verdi:")
                print("  Maksimumstemperatur (mnd):", df['Maksimumstemperatur (mnd)'][index - 1])
                print("\n")
                print("Neste rad verdi:")
                print("  Maksimumstemperatur (mnd):", df['Maksimumstemperatur (mnd)'][index + 1])
                print("Den nye verdien blir: ", interpolert_verdi)
            else:
                print("Ingen forrige eller neste rad å sammenligne med.")

            print("-" * 40)

    # Interpolerer NaN-verdier i 'Maksimumstemperatur (mnd)' og 'Minimumstemperatur (mnd)' kolonnene
    for kol in ['Maksimumstemperatur (mnd)', 'Minimumstemperatur (mnd)']:
        df[kol] = df[kol].interpolate(method='linear')

    #Lagrer dataene i en ny CSV-fil
    df.to_csv(fil_ut, sep=';', index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    fil_inn = "data/csv/Temp_data_Theim_14_25.csv"
    fil_ut = "data/csv/renset_tempdata_Theim.csv"

    # Sjekker om filen eksisterer
    try:
        rens_tempdata(fil_inn, fil_ut)
        print(f"Rensing fullført. Data lagret i '{fil_ut}'.")
    except Exception as e:
        print(f"En feil oppstod under rensing: {e}")