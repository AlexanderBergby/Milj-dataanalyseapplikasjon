import sys
import unittest
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from verdatavisuell_na import lagre_temperaturdata

class TestVerData(unittest.TestCase):
    def test_lagre_temperaturdata_oppretter_fil(self):
        test_fil = "data/json/test_temperatur.json"
        lagre_temperaturdata(test_fil)

        #Sjekker at filen faktisk ble opprettet.
        self.assertTrue(os.path.exists(test_fil))
        with open(test_fil, "r") as f:
            data = json.load(f)
        #Sjekker at dataen er en liste.
        self.assertIsInstance(data, list)
        #Sikrer at listen ikke er tom
        self.assertGreater(len(data), 0)
        #Sjekker at hvert element i lista inneholder både "city" og "temperature" som nøkler.
        self.assertIn("city", data[0])
        self.assertIn("temperature", data[0])

        #Fjerner testfilen
        os.remove(test_fil)

#Negativ test:
    def test_lagre_feil_filbane(self):
        with self.assertRaises(OSError):
            #If setning for å sjekke opprativsystem til brukeren
            #Tester en ugyldig filbane.
            if os.name == "nt":
                feil_filbane = "C:/Windows/ugyldig_mappe/test.json"
            else:
                feil_filbane = "/ugyldig_mappe/test.json"
            lagre_temperaturdata(feil_filbane)


if __name__ == "__main__":
    unittest.main()