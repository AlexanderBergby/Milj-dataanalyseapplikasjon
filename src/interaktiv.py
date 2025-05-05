import json
import pandas as pd
import plotly.express as px
from Værdata_nå import lagre_temperaturdata

#Oppdater temperaturdata før kart vises
lagre_temperaturdata()

# Last inn temperaturdata
with open("data/temperaturdata.json", "r") as f:
    temp_data = json.load(f)

df = pd.DataFrame(temp_data)

# Legg til koordinater
df["latitude"] = df["city"].map({
    "Oslo": 59.91,
    "Bergen": 60.39,
    "Trondheim": 63.43,
    "Stavanger": 58.97,
    "Tromsø": 69.65
})
df["longitude"] = df["city"].map({
    "Oslo": 10.75,
    "Bergen": 5.32,
    "Trondheim": 10.40,
    "Stavanger": 5.73,
    "Tromsø": 18.95
})

fig_geo = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    size='temperature',
    hover_name='city',
    color='temperature',
    color_continuous_scale='RdYlBu_r',
    projection="natural earth",
    title='Temperatur i store norske byer'
)

fig_geo.update_geos(
    scope="europe",
    lataxis_range=[57, 72],
    lonaxis_range=[4, 31],
    showcountries=True,
    countrycolor="LightGray"
)

fig_geo.show()
