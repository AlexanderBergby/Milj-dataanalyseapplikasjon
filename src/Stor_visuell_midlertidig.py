import pandas as pd
import plotly.graph_objects as go

# Leser inn data
df = pd.read_csv('data/csv/renset_tempdata_Theim.csv', sep=';', encoding='utf-8-sig')
df['Date'] = pd.to_datetime(df['Date'])

# Oppretter figur
fig = go.Figure()

# Legg til begge temperaturserier
fig.add_trace(
    go.Scatter(
        x=df['Date'], 
        y=df['Maksimumstemperatur (mnd)'], 
        name='Maksimum'))
fig.add_trace(
    go.Scatter(
        x=df['Date'], 
        y=df['Minimumstemperatur (mnd)'], 
        name='Minimum'))

# Sett tittel og x-akse med range slider og selectors (lik eksempelkoden)
fig.update_layout(
    title_text="Månedlig maksimums- og minimumstemperatur",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1 år", step="year", stepmode="backward"),
                dict(count=5, label="5 år", step="year", stepmode="backward"),
                dict(step="all", label="Alt")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date",
        
    ),
    yaxis=dict(title='Temperatur (°C)'),
    hovermode='x unified',
)

fig.show()
