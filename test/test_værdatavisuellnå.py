import sys
import unittest
import os
import json
from unittest.mock import patch

#gjør src tilgjengelig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from verdatavisuell_na import get_weather_data

class TestWeatherData(unittest.TestCase):
    #lager "fake" versjoner vi kan teste
    @patch("verdatavisuell_na.messagebox.showerror")
    @patch("verdatavisuell_na.requests.get")
    def test_get_weather_data_feilrespons(self, mock_get, mock_showerror):
        #simulere en API-feil
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {}

        data = get_weather_data(60, 10)
        #sjekker at funskjonene retunere NONE og feilmelding
        self.assertIsNone(data)
        mock_showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main()