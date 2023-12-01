import pandas as pd
import plotly.graph_objects as pl
from plotly.subplots import make_subplots
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process some integers.')

# Add the arguments
parser.add_argument('csv_file', type=str, help='The CSV file to process')
parser.add_argument('--id_pws', type=str, help='The id_pws to focus on. If not provided, all id_pws will be used.')

# Parse the arguments
args = parser.parse_args()

print(f'CSV file: {args.csv_file}')  # TESTING
print(f'id_pws: {args.id_pws}')  # TESTING


def read_csv(file, id_pws=None):
    print(f'Reading CSV file: {file}')  # TESTING
    column_names = ['temperature_fz', 'humidity_fz', 'pressure_fz', 'lat', 'long', 'time_gps', 'numSats_gps',
                     'temperature_pws', 'humidity_pws', 'time_pws', 'protocol_pws', 'id_pws']
    df = pd.read_csv(file, names=column_names, usecols=range(12))
    print(f'id_pws column: {df["id_pws"]}')  # TESTING
    print(f'Unique id_pws in the DataFrame before filtering: {df["id_pws"].unique()}')  # Add this line

    if id_pws is not None:
        print(f'Focusing on id_pws: {id_pws}')  # TESTING
        df = df[df['id_pws'] == float(id_pws)]  # Ensure id_pws is treated as a float
        print(f'Unique id_pws in the DataFrame after filtering: {df["id_pws"].unique()}')  # TESTING

        # Save the filtered DataFrame to a new CSV file
        filtered_file = f'filtered_{id_pws}.csv'
        df.to_csv(filtered_file, index=False)
        print(f'Filtered data saved to: {filtered_file}')  # TESTING

    return df


def plot_with_plotly(df):
    print('Plotting data...')  # TESTING

    # Create subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Temperature", "Humidity", "Pressure"))

    # sub plot lines
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_fz'], mode='markers', name='Temperature FZ'), row=1,
                  col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['temperature_pws'], mode='markers', name='Temperature PWS',
                             text=df.apply(lambda row: f'protocol_pws: {row.protocol_pws}, id_pws: {row.id_pws}',
                                          axis=1)), row=1, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_fz'], mode='markers', name='Humidity FZ'), row=2, col=1)
    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['humidity_pws'], mode='markers', name='Humidity PWS',
                             text=df.apply(lambda row: f'protocol_pws: {row.protocol_pws}, id_pws: {row.id_pws}',
                                          axis=1)), row=2, col=1)

    fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['pressure_fz'], mode='markers', name='Pressure FZ'), row=3, col=1)
    # fig.add_trace(pl.Scatter(x=df['time_gps'], y=df['pressure_pws'], mode='markers', name='Pressure PWS'), row=3,
    # col=1) # Currently no pressure from PWS

    # title at top
    fig.update_layout(title='Meteorological Data vs. Time')

    # x-axis title at the bottom
    fig.update_xaxes(title_text='Time', row=3, col=1)

    fig.update_yaxes(title_text=f'Temperature °C', row=1, col=1)
    fig.update_yaxes(title_text='Humidity %', row=2, col=1)
    fig.update_yaxes(title_text='Pressure hPa', row=3, col=1)

    # Show plot
    fig.show()


# use args.csv_file as the CSV file name
df = read_csv(args.csv_file, args.id_pws)
plot_with_plotly(df)
