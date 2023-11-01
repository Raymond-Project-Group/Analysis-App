# Raymond Project Group Analysis Application 

import pandas as pd
import plotly.graph_objects as pl
from plotly.subplots import make_subplots

def read_csv(file):
    column_names = ['temperature_fz', 'humidity_fz', 'pressure_fz', 'lat', 'long', 'time_gps', 'numSats_gps', 'temperature_pws', 'humidity_pws', 'time_pws', 'protocol_pws', 'id_pws']
    df = pd.read_csv(file, names=column_names, usecols=range(12))
    return df

def plot_with_plotly(df):
    # Create subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Temperature", "Humidity", "Pressure"))

    # sub plot lines
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_fz'], mode='lines', name='Temperature FZ'), row=1, col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_pws'], mode='lines', name='Temperature PWS'), row=1, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_fz'], mode='lines', name='Humidity FZ'), row=2, col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_pws'], mode='lines', name='Humidity PWS'), row=2, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['pressure_fz'], mode='lines', name='Pressure FZ'), row=3, col=1)
    # fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['pressure_pws'], mode='lines', name='Pressure PWS'), row=3, col=1) # Currently no pressure from PWS

    # title at top
    fig.update_layout(title='Meteorological Data vs. Time')

    # x-axis title at the bottom
    fig.update_xaxes(title_text='Time', row=3, col=1)
    
    fig.update_yaxes(title_text=f'Temperature °C', row=1, col=1)
    fig.update_yaxes(title_text='Humidity %', row=2, col=1)
    fig.update_yaxes(title_text='Pressure hPa', row=3, col=1)

    # Show plot
    fig.show()

df = read_csv('./sample_data.csv')
plot_with_plotly(df)
