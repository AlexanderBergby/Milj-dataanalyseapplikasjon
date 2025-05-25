import sys
import unittest
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from rensing import rens_tempdata
import tempfile


#Lager temporær csv fil med dummy verdier for testing
dummy_innhold = """Navn;Stasjon;Tid(norsk normaltid);Maksimumstemperatur (mnd);Minimumstemperatur (mnd)
Lade;SN68050;01.2014;8,7;-16,6
Lade;SN68050;02.2014;-;-7,9
Lade;SN68050;03.2014;12,6;-12,3
Lade;SN68050;04.2014;18,2;-4,1
Lade;SN68050;05.2014;22;-1,2
Lade;SN68050;06.2014;26,4;4,7
Lade;SN68050;07.2014;31,7;-
Lade;SN68050;08.2014;28,4;5,5
Lade;SN68050;09.2014;24;0
"""


class TestRensing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        #Linker til temporære filer, siden rens_tempdata tar inn filnavn som argumenter
        self.fil_inn = os.path.join(self.temp_dir.name, "fil_inn.csv")
        self.fil_ut  = os.path.join(self.temp_dir.name, "fil_ut.csv")

        with open(self.fil_inn, 'w', encoding='utf-8') as f:
            f.write(dummy_innhold)

        # Simulerer rensing av data
        rens_tempdata(self.fil_inn, self.fil_ut)

    def test_rensing_fildannelse(self):
        # Sjekker at den rensede filen er opprettet
        self.assertTrue(os.path.exists(self.fil_ut))

    def test_rensing_interpolering(self):
        # Leser inn den rensede filen
        df = pd.read_csv(self.fil_ut, sep=';', encoding='utf-8-sig')
        # Sjekker at NaN-verdier er interpolert
        self.assertFalse(df['Maksimumstemperatur (mnd)'].isna().any())
        self.assertFalse(df['Minimumstemperatur (mnd)'].isna().any())

        #Sjekker at interpolerte verdier stemmer
        forventet_maks = (8.7 + 12.6) / 2
        self.assertAlmostEqual(df['Maksimumstemperatur (mnd)'][1], forventet_maks, places=2)

        forventet_min = (4.7 + 5.5) / 2
        self.assertAlmostEqual(df['Minimumstemperatur (mnd)'][6], forventet_min, places=2)



    def tearDown(self):
        self.temp_dir.cleanup()


if __name__ == "__main__":
    
    unittest.main()