import sys
import unittest
import os

#gjør src tilgjengelig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from verdatavisuell_na import henter_vær_data

class TestVerData(unittest.TestCase):
    def test_ugyldige_koordinater(self):
        #Bruk helt usannsynlige koordinater
        data = henter_vær_data(-9999, -9999)

        #Forvent at funksjonen håndterer feilen og returnerer None
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
