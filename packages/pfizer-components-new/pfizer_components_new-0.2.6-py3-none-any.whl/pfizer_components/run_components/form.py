import os

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

current_directory = os.getcwd()
file_name = 'dbc.css'
file_path = os.path.join(current_directory, 'assets', file_name)

app = dash.Dash(external_stylesheets=[file_path])

app.layout = html.Div(
    style={'display': 'flex', 'align-items': 'center'},
    children=[
        html.Img(src='assets/iconimage.svg', style={'width': '461px', 'height': '528px'}),
        html.Div([html.H1('Find My Pfizer Medical Expert',
                          style={'margin-left': '24px', 'margin-top': '-5px', 'font-family': 'Noto Sans',
                                 'color': '#0000c9', 'fontSize': '32px',
                                 'width': '631px', 'height': '40px',
                                 'font-style': 'normal', 'font-weight': '300',
                                 'font-size': '32px', 'line-height': '40px',
                                 'letter-spacing': '0.25px'}),
                  html.Div(
                      "Pfizer Medical Experts are medical and scientific experts who enhance understanding of Pfizer research and the safe and appropriate use of Pfizer medicines and vaccines.",
                      style={'margin-left': '24px', 'width': 631, 'font-family': 'Noto Sans', 'fontSize': 16,
                             'height': 90, 'font-style': 'normal', 'font-weight': '400', 'font-size': '16px',
                             'line-height': '24px', 'letter-spacing': '0.25px', 'color': '#383838', 'flex': 'none',
                             'order': '0', 'align-self': 'stretch', 'flex-grow': '0'}),
                  html.Div(
                      'Fill in the details below to find a Pfizer Medical Expert in your area. Pfizer Medical Experts are available for select Disease States.',
                      style={'margin-left': '24px', 'margin-top': '10px', 'width': 631, 'font-family': 'Noto Sans',
                             'fontSize': 16,
                             'height': 54, 'font-style': 'normal', 'font-weight': '400', 'font-size': '16px',
                             'line-height': '24px', 'letter-spacing': '0.25px', 'color': '#383838', 'flex': 'none',
                             'order': '0', 'align-self': 'stretch', 'flex-grow': '0'}),
                  dbc.Row(
                      dbc.Col([
                          # putting two dropdown in div
                          html.Div([html.Div([html.H1(className='Therapy Area ', children="Therapy Area *",
                                                      style={'font-family': 'Noto Sans', 'whiteSpace': 'nowrap',
                                                             'fontSize': '16px'}),
                                              dcc.Dropdown(className='custom-dropdown',
                                                           options=[{'label': 'JAN', 'value': 'M1'},
                                                                    {'label': 'FEB', 'value': 'M2'},
                                                                    {'label': 'MAR', 'value': 'M3'},
                                                                    {'label': 'APR', 'value': 'M4'},
                                                                    {'label': 'MAY', 'value': 'M5'},
                                                                    {'label': 'JUN', 'value': 'M6'},
                                                                    {'label': 'JUL', 'value': 'M7'},
                                                                    {'label': 'AUG', 'value': 'M8'},
                                                                    {'label': 'SEP', 'value': 'M9'}],
                                                           placeholder='Select therapy area *',
                                                           clearable=False,
                                                           style={'font-family': 'Noto Sans'})]),
                                    html.Div([html.H1(className='Therapy Area ', children="Disease State *",
                                                      style={'font-family': 'Noto Sans', 'whiteSpace': 'nowrap',
                                                             'fontSize': '16px', 'margin-left': '18px'}),
                                              dcc.Dropdown(className='Disease State *',
                                                           options=[{'label': 'JAN', 'value': 'M1'},
                                                                    {'label': 'FEB', 'value': 'M2'},
                                                                    {'label': 'MAR', 'value': 'M3'},
                                                                    {'label': 'APR', 'value': 'M4'},
                                                                    {'label': 'MAY', 'value': 'M5'},
                                                                    {'label': 'JUN', 'value': 'M6'},
                                                                    {'label': 'JUL', 'value': 'M7'},
                                                                    {'label': 'AUG', 'value': 'M8'},
                                                                    {'label': 'SEP', 'value': 'M9'}],
                                                           placeholder='Select disease state',
                                                           clearable=False,
                                                           style={'font-family': 'Noto Sans',
                                                                  'margin-left': '6px'})]), ],
                                   style={'margin-left': '24px', 'margin-top': '32px', 'display': 'flex',
                                          'align-items': 'center'}),
                          # input starts here
                          html.H1(id="input-text2", children='Zip Code *',
                                  style={'margin-left': '24px', 'margin-top': '24px', 'Ag': 'font-size-700/bold',
                                         'height': 18, 'width': 36,
                                         'font-family': 'Noto Sans',
                                         'font-weight': 700, 'fontSize': 16, 'line-height': 18, 'letter': '-0.5px',
                                         'whiteSpace': 'nowrap'}),
                          dcc.Input(id='my-input',
                                    type='text',
                                    placeholder='Enter zip code',
                                    className='my-input',
                                    style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 400,
                                           'font-size': 17, 'line-height': 24, 'letter': '-0.5px',
                                           'border': 'Transparent', 'margin-left': '24px'},
                                    min='5',
                                    max='100',
                                    maxLength=10,
                                    ),
                      ],
                          className="mb-3"
                      )
                  ),
                  html.Button('Submit', id='Large',
                              style={'background-color': '#003FE2', 'font-family': 'NOTO SANS', 'display': 'flex',
                                     'flex-direction': 'row', 'justify-content': 'center', 'align-item': 'center',
                                     'padding': '16px 32px', 'gap': '12px', 'position': 'relative', 'width': '153px',
                                     'height': '56px', 'background': '#003FE2', 'border-radius': '1px',
                                     'font-weight': '700', 'font-size': '17px', 'line-height': '24px',
                                     'letter-spacing': '-0.5px',
                                     'color': '#FFFFFF', 'border': 'none', 'margin-left': '24px',
                                     'margin-top': '24px'}),
                  ])
    ]
)

if __name__ == '__main__':
    app.run_server(port=8323, debug=True)
