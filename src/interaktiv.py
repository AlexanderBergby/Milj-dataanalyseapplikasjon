import json
import pandas as pd
import plotly.express as px
from Værdata_nå import lagre_temperaturdata

# Oppdater temperaturdata
lagre_temperaturdata()

# Last inn temperaturdata
with open("data/temperaturdata.json", "r") as f:
    temp_data = json.load(f)

df = pd.DataFrame(temp_data)

# Legg til koordinater
koord = {
    "Oslo": (59.91, 10.75),
    "Bergen": (60.39, 5.32),
    "Trondheim": (63.43, 10.40),
    "Stavanger": (58.97, 5.73),
    "Tromsø": (69.65, 18.95)
}
df["latitude"] = df["city"].map(lambda x: koord[x][0])
df["longitude"] = df["city"].map(lambda x: koord[x][1])

# Vi sender bare det vi vil vise til hover med custom_data
fig_geo = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    size='temperature',
    size_max=30,
    color='temperature',
    color_continuous_scale='RdYlBu_r',
    projection="natural earth",
    custom_data=['city', 'temperature'],  # ✅ Bare disse sendes til hover
    title='🌡️ Temperatur i store norske byer'
)

# Vi lager vårt eget hovertemplate
fig_geo.update_traces(
    marker=dict(line=dict(width=1, color='white')),
    hovertemplate='<b>%{customdata[0]}</b><br>Temperatur: %{customdata[1]} °C<extra></extra>'
)

fig_geo.update_geos(
    scope="europe",
    lataxis_range=[57, 72],
    lonaxis_range=[4, 31],
    showcountries=True,
    countrycolor="LightGray"
)

fig_geo.update_layout(
    font=dict(size=16),
    title_font=dict(size=22),
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
)

fig_geo.show()
