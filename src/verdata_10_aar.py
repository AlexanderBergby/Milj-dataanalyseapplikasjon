"""
verdata_10_aar.py
Dette skriptet visualiserer månedlig maksimums- og minimumstemperatur for Lade i Trondheim
fra 2014 til 2025 ved hjelp av Plotly."""

import pandas as pd
import plotly.graph_objects as go

def vis_temperaturgraf():
    # Leser inn data
    df = pd.read_csv('data/csv/renset_tempdata_Theim.csv', sep=';', encoding='utf-8-sig')
    df['Date'] = pd.to_datetime(df['Date'])

    # Oppretter figur
    fig = go.Figure()

    # Legger til maksimums- og minimumstemperatur som scatter plots
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

    # Setter tittel og x-akse med range slider og knapper (lik eksempelkoden fra Plotly)
    fig.update_layout(
        title_text="Månedlig maksimums- og minimumstemperatur for Lade i Trondheim (2014-2025)",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 år", step="year", stepmode="backward"),
                    dict(count=5, label="5 år", step="year", stepmode="backward"),
                    dict(step="all", label="Alt")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(title='Temperatur (°C)'),
        hovermode='x unified'
    )

    fig.show()

