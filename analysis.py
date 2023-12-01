import pandas as pd
import plotly.graph_objects as pl
from plotly.subplots import make_subplots
import argparse
import math

# Create the parser
parser = argparse.ArgumentParser(description='Process some integers.')


# Add the arguments
parser.add_argument('csv_file', type=str, help='The CSV file to process')
parser.add_argument('--id_pws', type=str, help='The id_pws to focus on. If not provided, all id_pws will be used.')
parser.add_argument('--tu', type=str, choices=['c', 'f'], default='c', help='The unit for temperature. If not provided, Celsius will be used.')
parser.add_argument('--hu', type=str, choices=['r', 'a'], default='r', help='The unit for humidity. If not provided, percentage will be used.')

# Parse the arguments
args = parser.parse_args()

print(f'CSV file: {args.csv_file}')  # TESTING
print(f'id_pws: {args.id_pws}')  # TESTING
print(f'Temperature unit: {args.tu}')  # TESTING
print(f'Humidity unit: {args.hu}')  # TESTING


def read_csv(file, id_pws=None, temp_unit='c', hum_unit='r'):
    print(f'Reading CSV file: {file}')  # TESTING
    column_names = ['temperature_fz', 'humidity_fz', 'pressure_fz', 'lat', 'long', 'time_gps', 'numSats_gps',
                     'temperature_pws', 'humidity_pws', 'time_pws', 'protocol_pws', 'id_pws']
    df = pd.read_csv(file, names=column_names, usecols=range(12))

    # Convert humidity from relative humidity to absolute humidity if --hu=a
    # This is a simplified formula and might not be accurate for all conditions
    if hum_unit == 'a':
        df['humidity_fz'] = df.apply(lambda row: absHumid(row['humidity_fz'], row['temperature_fz']), axis=1)
        df['humidity_pws'] = df.apply(lambda row: absHumid(row['humidity_pws'], row['temperature_pws']), axis=1)

    # Convert temperature from Celsius to Fahrenheit if --tu=f
    if temp_unit == 'f':
        df['temperature_fz'] = celsius_to_fahrenheit(df['temperature_fz'])
        df['temperature_pws'] = celsius_to_fahrenheit(df['temperature_pws'])

    # Save the DataFrame to a new CSV file
    df.to_csv('new_' + file, index=False)

    return df


def plot_with_plotly(df, temp_unit='c', hum_unit='r'):
    print('Plotting data...')  # TESTING

    # Set the Y-axis labels based on the temp_unit and hum_unit arguments
    temp_label = 'Temperature (°F)' if temp_unit == 'f' else 'Temperature (°C)'
    hum_label = 'Humidity (%Absolute)' if hum_unit == 'a' else 'Humidity (%Relative)'

    # Create subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=(temp_label, hum_label, "Pressure"))

    # sub plot lines
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_fz'], mode='markers', name='Temperature FZ'), row=1, col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_pws'], mode='markers', name='Temperature PWS', text=df.apply(lambda row: f'protocol_pws: {row.protocol_pws}, id_pws: {row.id_pws}', axis=1)), row=1, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_fz'], mode='markers', name='Humidity FZ'), row=2, col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_pws'], mode='markers', name='Humidity PWS', text=df.apply(lambda row: f'protocol_pws: {row.protocol_pws}, id_pws: {row.id_pws}', axis=1)), row=2, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['pressure_fz'], mode='markers', name='Pressure FZ'), row=3, col=1)

    # title at top
    fig.update_layout(title='Meteorological Data vs. Time')

    # x-axis title at the bottom
    fig.update_xaxes(title_text='Time', row=3, col=1)
    fig.update_yaxes(title_text=temp_label, row=1, col=1)
    fig.update_yaxes(title_text=hum_label, row=2, col=1)
    fig.update_yaxes(title_text='Pressure hPa', row=3, col=1)

    # Show plot
    fig.show()

def absHumid(humid,temp):
   pc = 22.0640 * 1000000 #Critical Pressure in Pa
   tc = 647.096 #Critical Temperature in Kelvin 
   t = temp + 273.15
   a1 = -7.85951783
   a2 = 1.84408259
   a3 = -11.7866497
   a4 = 22.6807411
   a5 = -15.9618719
   a6 = 1.80122502
   tau = 1 - t/tc
   ps = pc * math.exp((tc/t) * (a1*tau + a2*pow(tau,1.5) + a3*pow(tau,3) + 
                                a4*pow(tau,3.5)+a5*pow(tau,4) + a6*pow(tau,7.5)))
   rw = 461.5 # Specific gas constant in J/(kg K)
   pa = ps * humid/100
  #return pa
   return pa*1000/(rw*t) #returns in g/(m^3)

def celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

# use args.csv_file as the CSV file name
df = read_csv(args.csv_file, id_pws=args.id_pws, temp_unit=args.tu, hum_unit=args.hu)

plot_with_plotly(df, temp_unit=args.tu, hum_unit=args.hu)