import pandas as pd
import plotly.express as px

data = {
    'city': ['Oslo', 'Bergen', 'Trondheim', 'Stavanger', 'Tromsø'],
    'latitude': [59.91, 60.39, 63.43, 58.97, 69.65],
    'longitude': [10.75, 5.32, 10.40, 5.73, 18.95],
    'temperature': [30, 12, 10, 11, 8]  # Eksempeltemperaturer, TODO: erstatt med faktiske data
}

df = pd.DataFrame(data)

fig_geo = px.scatter_geo(
    df,
    lat='latitude',
    lon='longitude',
    size='temperature',
    hover_name='city',
    color='temperature',
    color_continuous_scale=[(0, "#a6cee3"), (1, "#ff9999")],
    projection="natural earth",
    title='Gjennomsnittstemperatur for store norske byer'
)

# Oppdater kartets geografi for å fokusere på Norge
fig_geo.update_geos(
    scope="europe",
    lataxis_range=[57, 72],
    lonaxis_range=[4, 31],
    showcountries=True,
    countrycolor="LightGray" 
)

fig_geo.show()
