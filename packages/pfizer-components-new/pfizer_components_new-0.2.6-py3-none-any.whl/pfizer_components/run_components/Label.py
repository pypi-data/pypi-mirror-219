import os
from dash import Dash, html
import dash_bootstrap_components as dbc

current_directory = os.getcwd()
file_name = 'assets/style.css'
file_path = os.path.join(current_directory, '../assets', file_name)

app = Dash(__name__, external_stylesheets=[file_path])

app.layout = html.Div([
    # Label above the radio buttons
    html.Label('Label', style={'font-family': 'Noto Sans', 'padding': '5px'}),
    dbc.RadioItems(
        options=[
            {'label': 'New York City', 'value': '1', 'title': 'Label1'},
            {'label': 'Montreal', 'value': '2', 'title': 'Label2'},
        ], style={'font-family': 'Noto Sans'},
        inputCheckedStyle={"accent-color": "#003Fe2"},
        input_style={'border-color': "yellow"}
    ),
    dbc.RadioItems(
        options=[
            {'label': 'Bangalore', 'disabled': True}],
        style={'font-family': 'Noto Sans'},
        className='special-radio-item',
    ),
])

if __name__ == "__main__":
    app.run_server(port=8121, debug=True)
