Her er en beskrivelse av de ulike filene som eksisterer i mappen "data". To undermapper er laget for å dele inn i ulike filtyper, csv og json. 

CSV
- weather_data.csv
Denne inneholder data for de siste 7 dagene i Trondheim (temperatur, nedbør og vind) fra meterologisk institutt sin api ,hentet ved å bruke Verdata_uke skriptet, dataene oppdateres hver gang skriptet kjøres.  

- Temp_data_Theim_14_25.csv
Denne inneholder maks og minimumstemperatur for Trondheim (Lade) de siste 10 årene og er hentet direkte som en csv fil fra MET. Denne csv-filen inneholder urenset data, og blir renset i rensing.py. 

- renset_tempdata_Theim.csv
Renset versjon av Temp_data_Theim_14-25, brukes i verdata_10_aar, Nan verdier er fylt inn vha interpolering.

JSON
- temperaturdata.json
Inneholder data for temperaturen akkurat nå i de fem sørste byene i Norge som hentes ved bruk av API og oppdateres derfor hver gang skriptet kjøres. Dataene brukes av interaktiv.py