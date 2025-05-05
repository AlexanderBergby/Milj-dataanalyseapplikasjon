Her er en kort beskrivelse av de ulike filene som eksisterer i mappen "src". Se kommentarer i filene for mer detaljert beskrivelse.

- Værdata_uke.py
Dette scriptet tar inn en API, lagrer data for de siste 7 dagene til tre elementer (temperatur, nedbør og vind) fra json filen, beregner deretter diverse statistikker for temperaturer som minimum, maksimum, gjennomsnitt, median og standardavvikpresenterer og lagrer som en csv fil ved hjelp av Pandas.

    Her har vi brukt følgende API: https://frost.met.no/howto.html 
    Dette anser vi som en pålitelig og bra kilde da det er en ofisiell side fra meteorologisk institutt. 

    Vi måtte lage bruker, og fikk da følgene "Client credentials":
    ID: e1e74478-764e-4bac-8a69-f70fe2ed8c6d
    Secret: 29556497-9e34-4403-bcbe-0e406da014ee

- Værdata_nå.py
    Dette Python-skriptet henter værdata for Oslo, Trondheim og Bergen i nåtid fra METs vær-API og sjekker basert på progrnose data fra API'et om det kommer til å bli regn de neste 2 timene

    Henting av data: Skriptet sender en GET-forespørsel til MET sitt API med posisjonsparametere for Oslo, Trondheim eller Bergen basert på brukerens ønske.

    Første måling: Den første oppføringen i API-responsen (nåværende værdata) skrives ut med detaljert informasjon som lufttemperatur, nedbør, relativ luftfuktighet og vinddata.

    Regnsjekk: Skriptet går gjennom de resterende målingene (som dekker de neste 2 timene) og sjekker om precipitation_rate er ulik 0. Hvis minst én måling indikerer nedbør, skrives det ut at det kommer regn; ellers vises en melding om at det ikke blir regn.

- Værdata_nå_visuell.py

    Viser værdataen til en bruker på en simpel måte med å bruke tkinter, det endelige målet er å slå sammen værdata_nå og værdata_nå_visuell i en og bruke denne i en hovedmeny som kommer senere

- Visualisering.py

    Henter værdata fra CSV-filen laget i værdata_uke og produserer to grafer som visualiserer temperaturstatistikk og forholdet mellom gjennomsnittstemperatur og vindhastighet, den regner også ut korrelasjonen mellom gjennomsnittemperaturen og vindhasitgheten

- Luftkvalitet.py

    Tar inn API som har data for flere ulike AQI (Air quality indekser)
    Lager en graf for no2, pm10, pm25, o3 og en overall AQI, dette er en varsel from fremtidig luftkvalitet

- Prediktiv_analyse (akkurat startet på, ikke fullført)

    Bruker en lineær regresjonsmodell for å predikere gjennomsnittstemperatur basert på vindhastighet og nedbør ved å benytte data fra værdata lagret i CSV_filen
    Nåværende resultater (RMSE = 4.6, som angir gjennomsnittlig avvik mellom modellens prediksjoner og de faktiske verdiene, og R^2-score = -10,32, som viser hvor godt modellen fanger variasjoner i dataen) er prediksjonen veldig dårlig nå. Mtp på at værdataene varierer fra ca -0.5 til 14 grader er avviket på 4.6 veldig høyt. Vi håper derfor med videre utvikling der vi skal ta inn mange flere data at prediksjonen blir bedre

- Interaktiv

    Bruker funksjonen definert i værdata_nå til å hente temperaturen til norges 5 største byer. Disse er blitt lagret i en json fil i data-mappen. Vi bruker Plotly Express med scatter_geo() sammen med spesifikasjonen scope="europe" for å vise et Europakart og json filen med temperaturen for å visuelt vise tempraturen pent. 