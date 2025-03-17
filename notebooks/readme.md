Her er en kort beskrivelse av de ulike filene som eksisterer i mappen "notebooks". Se kommentarer i filene for mer detaljert beskrivelse.

- Værdata_uke.py
Dette scriptet tar inn en API, lagrer data for de siste 7 dagene til tre elementer (temperatur, nedbør og vind) fra json filen, presenterer dette visuelt i form av skrift og lagrer som en csv fil ved hjelp av Pandas.

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

- Visualisering.py

Lager en graf som viser gjennomsnittstemp og max/min område for været siste uken. 

-luftkvalitet.py

Tar inn API som har data for flere ulike AQI (Air quality indekser)
Lager en graf for no2, pm10, pm25, o3 og en overall AQI, dette er en varsel from fremtidig luftkvalitet