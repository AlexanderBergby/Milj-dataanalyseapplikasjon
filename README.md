# Milj-dataanalyseapplikasjon
Prosjekt TDT4114, miljødataanalyseapplikasjon, Gruppe 107

Dette er Python-program som samler inn, analyserer og visualiserer vær- og miljødata, med et grafisk brukergrensesnitt (GUI) laget i Tkinter. Programmet gjør det enkelt å hente sanntidsvær, vise statistikk for siste uke, lage interaktive grafer og utføre enkel prediktiv analyse – alt via en brukervennlig meny.

Mappestrukturen vår seg følgende ut: 
Milj-dataanalyseapplikasjon/
├── data/                #Rådata og analyserte data (CSV/JSON)
├── docs/                #Viktige dokumenter (pdf og md)
├── resources/           #Bakgrunnsbilde brukt i GUI-menyen
├── src/                 #All kode og hovedmeny (meny_gui.py)
├── test/                #Enhetstester for ulike funksjoner
├──.gitignore            #gitignore fil
├──README.md             #denne filen
└── requirements.txt     #pakker/krav til å kunne kjøre koden
Alle mappene inneholder egen readme.md med beskrivelse av mappens innhold.


Det er to ulike metoder for å kjøre programmet vårt:
1.  Skriv inn følgene i terminalen:
python3 src/meny_gui.py

2. Kjør koden meny_gui.py, som ligger i src mappen.

En beskrivelse av menyen og dens innhold: 
"1 - Værmelding-Norske byer" 
Henter sanntidsdata for de 5 største byene i Norge.
(Bruk av API)
"2 - Værdata for Trondheim"
Viser værmelding for Trondheim for de siste 7 dagene som både tekst og figur. 
(Bruk av API)
"3 - Prediktiv analyse"
Enkel værprediksjon for makstemperaturen den påfølgene måneden (sklearn). 
"4 - Luftkvalitet"
Viser luftforurensning. (Bruk av API)
"5 - Interaktiv visning"
Plotly-graf for temperaturen i de 5 største byene i Norge.
"6 - Temperatur siste 10 årene"
Historisk temperaturutvikling som interaktiv graf.

