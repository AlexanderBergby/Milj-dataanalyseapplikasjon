# Milj-dataanalyseapplikasjon
Prosjekt TDT4114, miljødataanalyseapplikasjon

Del 1: Datainnsamling og forberedelse

Oppgave 1: I oppgave 1 lagde gruppen et felles Repo, hvor vi har laget oss en Main og to individuelle branches kalt "Serina" og "Alex". 

Oppgave 2: Datainnsamling
Gruppen valgte å bruke "Metrologisk institutt" sin API. Gruppen så igjennom ulike altarnativer for datainnsamlingsnettsider hvor de viktigste kriteriene var: 
- Tilgjengelighet
- Kvalitet 
- Pålitelighet

Gruppen anser MET til å være både svært pålitelighet og av god kvalitet. 

Dataen som ble hentet fra denne API-en er:
- Temperatur
- Nedbør
- Vindhastighet

Oppgave 3: Databehandling

Gruppen har brukt pandas for å lagre data i en csv fil for å senere bruke dette i visualisering av dataen. 

Gruppen kan forvente outliers (-50 eller +50 pga f.eks skrivefeil), manglende data eller inkonsekvente enheter (km/t eller m/s).
I fremtidig behandling av dataen (innlevering av del 2) kan vi bruke:
- sette logiske grenser for temp
- df.isnull().sum() for å se antall manglende verdier (NaN) i hver kolonne.
- videre kan vi bruke dropna/fillna/interpolate for å fylle manglende data

List comprehensions:
- Kan integreres for å sjekke og rette opp i inkonsekvente enheter.



