import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leser data fra CSV-fil, som er lagret i UTF-8, og med semikolon som separator, holder kolonnen 'Tid(norsk normaltid)' som str
df = pd.read_csv(
    'data/csv/Temp_data_Theim_14_25.csv',
    sep=';',
    encoding='utf-8-sig',
    dtype={'Tid(norsk normaltid)': str}
)
df['Date'] = pd.to_datetime(df['Tid(norsk normaltid)'], format='%m.%Y')

# Renser data, endrer ',' til '.' (Må gjøre for å bruke pandas) og '-' til NaN, og konverterer til float
for kol in ['Maksimumstemperatur (mnd)', 'Minimumstemperatur (mnd)']:
    rådata = df[kol].astype(str) 
    # Bytt ut '-' med np.nan
    df[kol] = rådata.replace('-', np.nan)
    
     #Bytt ut komma med punktum
    df[kol] = df[kol].str.replace(',', '.', regex=False)

    # Konverter til flyttall (float)
    df[kol] = df[kol].astype(float)


# Kun for å illustrere at det er NaN i dataene, og sjekker at rensingen er gjort riktig
for index in range(len(df)):
    min_value = df['Minimumstemperatur (mnd)'][index]
    max_value = df['Maksimumstemperatur (mnd)'][index]

    # Sjekker om det er NaN i dataene
    if pd.isna(min_value) or pd.isna(max_value):
        print("NaN i: ", index)
        print("Maksimumstemperatur (mnd):", max_value)
        print("Minimumstemperatur (mnd):", min_value)

        # Hvis det ikke er den første raden, skriv ut verdiene fra forrige rad
        if index > 0:
            print("Forrige rad verdi:")
            print("  Maksimumstemperatur (mnd):", df['Maksimumstemperatur (mnd)'][index - 1])
            print("  Minimumstemperatur (mnd):", df['Minimumstemperatur (mnd)'][index - 1])

        # Hvis det ikke er den siste raden, skriv ut verdiene fra neste rad
        if index < len(df) - 1:
            print("Neste rad verdi:")
            print("  Maksimumstemperatur (mnd):", df['Maksimumstemperatur (mnd)'][index + 1])
            print("  Minimumstemperatur (mnd):", df['Minimumstemperatur (mnd)'][index + 1])

        print("-" * 40)

# Interpolerer NaN-verdier i 'Maksimumstemperatur (mnd)' og 'Minimumstemperatur (mnd)' kolonnene
for kol in ['Maksimumstemperatur (mnd)', 'Minimumstemperatur (mnd)']:
    df[kol] = df[kol].interpolate(method='linear')




df.to_csv('data/csv/renset_tempdata_Theim.csv', sep=';', index=False, encoding='utf-8-sig')
