Her er en kort beskrivelse av de ulike filene som eksisterer i mappen "src". Se kommentarer i filene for mer detaljert beskrivelse.

- interaktiv.py
    Bruker funksjonen fra verdatavisuell_na.py til å hente og vise temperatur i de fem største byene i Norge (Oslo, Bergen, Trondheim, Stavanger og Tromsø). Dataene visualiseres på et kart over Europa ved hjelp av plotly.express. 

- luftkvalitet.py
    Henter og visualiserer luftkvalitet prognoser for NO2, PM10, PM2.5, O3 og total AQI med matplotlib og seaborn.

- prediktiv_analyse.py
    Bygger en lineær regresjonsmodell for å predikere neste måneds maksimumstemperatur, basert på data fra 10 år tilbake. Viser resultater i GUI og graf.   

- rensing.py
    Renser og forbehandler rå CSV-temperaturdata: konverterer verdier manglende verdier ("-") til NaN og fyller inn manglende data vha interpolering

- utliggere.py
    Finner og skriver ut utliggere i maksimumstemperaturer ved bruk av IQR-metoden.

- verdata_10_aar.py
    Visualiserer temperaturutvikling over 10 år med interaktiv plotly-graf.

- Værdata_uke.py
    Henter værdata for Trondheim (Granåsen) fra siste 7 dager og beregner statistikk: min, maks, snitt, median og standardavvik. Lagres i CSV og vises i GUI.

    Her har vi brukt følgende API: https://frost.met.no/howto.html 
    Dette anser vi som en pålitelig og bra kilde da det er en ofisiell side fra meteorologisk institutt. 

    Vi måtte lage bruker, og fikk da følgene "Client credentials":
    ID: e1e74478-764e-4bac-8a69-f70fe2ed8c6d
    Secret: 29556497-9e34-4403-bcbe-0e406da014ee

    I denne koden beregnes blant annet median, gjennomsnitt og standardavvik.
    Median, gjennomsnitt og standardavvik gir viktig innsikt i datasettets fordeling og variasjon. Gjennomsnitt viser den typiske verdien, men kan påvirkes av ekstreme verdier. Median er den midterste verdien og er nyttig for datasett med store avvik. Standardavvik måler variasjonen rundt gjennomsnittet og hjelper med å vurdere usikkerheten i dataene. Disse målene er viktige for å forstå mønstre og variasjon i datasettet.

- Verdatavisuell_na.py
    GUI som henter og viser sanntidsdata (temperatur, nedbør, vind osv.) for fem norske byer. Data lagres også i JSON.

- Visualisering.py
    Leser værdata fra CSV og viser temperaturutvikling med min/maks-område, gjennomsnitt, median og standardavvik.





