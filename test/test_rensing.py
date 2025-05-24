import sys
import unittest
import os
import json
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from rensing import rens_tempdata

#Lager Dataframe for test

df = pd.DataFrame({
    'Maksimumstemperatur (mnd)': ['-1,5', '2,0', '-', '3,5', '4,0'],
    'Minimumstemperatur (mnd)': ['-2,0', '-', '1,0', '2,5', '3,0']
})

class TestRensing(unittest.TestCase):
    def setUp(self):
        self.fil_inn = "data/csv/Temp_data_Theim_14_25.csv"
        self.fil_ut = "data/csv/renset_tempdata_Theim.csv"
        # Simulerer rensing av data
        rens_tempdata(self.fil_inn, self.fil_ut)

    def test_rens_tempdata(self):
        # Leser inn den rensede filen
        df_renset = pd.read_csv(self.fil_ut, sep=';', encoding='utf-8-sig')
        
        # Sjekker at NaN-verdier er interpolert
        self.assertFalse(df_renset['Maksimumstemperatur (mnd)'].isnull().any())
        self.assertFalse(df_renset['Minimumstemperatur (mnd)'].isnull().any())
