import unittest
import os
import pandas as pd
import sys
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from Verdata_uke import værdata_uke

class TestVærdataUkeMinimal(unittest.TestCase):
    def test_weather_data_csv_innhold(self):
        filnavn = "data/weather_data.csv"

        #Kjører funksjonen som genererer CSV
        værdata_uke()

        #Sjekker at filen ble opprettet
        self.assertTrue(os.path.exists(filnavn))

        #Sjekker at innholdet er riktig strukturert
        df = pd.read_csv(filnavn)
        forventede_kolonner = {
            "date", "min_temp", "max_temp", "avg_temp",
            "median_temp", "std_temp", "precipitation", "wind_speed"
        }

        self.assertTrue(forventede_kolonner.issubset(df.columns))
        self.assertGreaterEqual(len(df), 1)

    #Negativ test med en "mock"fil
    @patch("pandas.DataFrame.to_csv", side_effect=OSError("Kan ikke lagre fil"))
    def test_feil_ved_lagring(self, mock_csv):
        with self.assertRaises(OSError):
            værdata_uke()

if __name__ == "__main__":
    unittest.main()
