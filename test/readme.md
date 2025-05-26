Her er en kort beskrivelse av de ulike filene som eksisterer i mappen "test". Se kommentarer i koden for mer detaljer.

Testene kjøres seperat i hver sin .py fil.

- test_lagre_temperatur.py
Dette skriptet inneholder enhetstester for funksjonen lagre_temperaturdata fra verdatavisuell_na.py. Testene er skrevet med unittest og validerer at funksjonen lagrer korrekt strukturert temperaturdata i json-format. Negativ test for feil filbane (OSError).

- test_rensing.py
Dette testystemet innegolder enhetstester for funksjonen rens_tempdata i rensing.py. Testen lager en dummy-csv fil med dummy-verdier for testing. Tester at en renset fil blir laget, og at rensing skjer slik som i rensing.py viser. Sjekker også at inerpolerte verdier er gjort riktig, og at temperaturer er i float-format. 

- test_verdatauke.py
Dette testsystemet verifiserer funksjonen værdata_uke fra Verdata_uke.py, som henter, analyserer og lagrer værdata til CSV-format. Simulerer skrivefeil med mock (negativ test).


- test_værdatavisuellnå.py
Dette testsystemet verifiserer funksjonen get_weather_data fra verdatavisuell_na.py, som henter værdata via API og håndterer feil. Sjekker at feilmelding vises med messagebox.showerror.
