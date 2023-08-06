import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.layout = html.Span([
    dbc.Button(
        [dbc.Badge("0", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}
                   )], color="danger", style={'background-color': '#003FE2', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px'}),
    dbc.Button(
        [dbc.Badge("0", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#858D97'}
                   )], color="danger", style={'background-color': '#DEE0E6', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px'}),
    dbc.Button(
        [dbc.Badge("00", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}
                   )], color="danger", style={'background-color': '#003FE2', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px'}),
    dbc.Button(
        [dbc.Badge("000", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}
                   )], color="danger", style={'background-color': '#003FE2', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px'}),
    dbc.Button(
        [dbc.Badge("1k", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}
                   )], color="danger", style={'background-color': '#003FE2', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px'}),
    dbc.Button(
        [dbc.Badge("NEW", class_name="ms-1",
                   style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                          'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}
                   )], color="danger", style={'background-color': '#003FE2', 'border-radius': '10px',
                                              'position': 'relative', 'border': 'none', 'margin-left': '10px', })
])

if __name__ == "__main__":
    app.run_server(port=8234, debug=True)
