from dash import html, dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.layout = dbc.Container([
    dbc.Alert([
        html.I(className="fas fa-exclamation-circle"),
        html.Span("🔴  This is an alert message",
                  style={'width': '196px', 'height': '24px', 'fontFamily': 'Noto Sans', 'fontWeight': '700',
                         'fontSize': '17px', 'lineHeight': '24px', 'letterSpacing': '-0.5px',
                         'whiteSpace': 'nowrap', 'padding': '11px 0px 0px 0px'})],
              color="secondary",
              style={'height': 48, 'width': 256, 'display': 'flex', 'flex-direction': 'row',
                     'align-items': 'flex-start', 'padding': '12px 16px', 'gap': '12px', 'position': 'relative',
                     'background': '#F2F2F8', 'border-radius': '2px'}),
    dbc.Alert([html.I(className="fas fa-exclamation-circle"),
               html.Span("🔴  This is an alert message",
                         style={'width': '160px', 'height': '18px', 'fontFamily': 'Noto Sans', 'fontWeight': '700',
                                'fontSize': '14px', 'lineHeight': '18px', 'letterSpacing': '-0.5px',
                                'whiteSpace': 'nowrap', 'padding': '9px 0px 0px 0px'})],
              color="primary",
              style={'height': 34, 'width': 220, 'display': 'flex', 'flex-direction': 'row',
                     'align-items': 'flex-start', 'padding': '12px 16px', 'gap': '12px', 'position': 'relative',
                     'background': '#F2F2F8', 'border-radius': '2px', 'margin-top': '24px',
                     }),
    dbc.Alert([html.I(className="fas fa-exclamation-circle"),
               html.Span("🔴  This is a toast message that wraps to multiple lines",
                         style={'width': '270px', 'height': '48px', 'fontFamily': 'Noto Sans', 'fontWeight': '700',
                                'fontSize': '17px', 'lineHeight': '24px', 'letterSpacing': '-0.5px',
                                'padding': '-8px 0px 12px 0px', 'margin-top': '-8px', 'alignItems': 'flex-start'})],
              color="primary",
              style={'height': 34, 'width': 308, 'display': 'flex', 'flex-direction': 'row',
                     'align-items': 'flex-start', 'padding': '12px 16px', 'gap': '12px', 'position': 'relative',
                     'background': '#F2F2F8', 'border-radius': '2px', 'margin-top': '24px'}),
    dbc.Alert([html.I(className="fas fa-exclamation-circle"),
               html.Span("This is a toast message that wraps to multiple lines",
                         style={'width': '289px', 'height': '48px', 'fontFamily': 'Noto Sans', 'fontWeight': '700',
                                'fontSize': '17px', 'lineHeight': '24px', 'letterSpacing': '-0.5px',
                                'padding': '-8px 0px 12px 0px', 'margin-top': '-8px', 'flex': 'none',
                                'order': '1', 'flex-grow': '1', 'alignItems': 'flex-start'})],
              color="primary",
              style={'height': 34, 'width': 321, 'display': 'flex', 'flex-direction': 'row',
                     'align-items': 'flex-start', 'padding': '12px 16px', 'gap': '12px', 'position': 'relative',
                     'background': '#F2F2F8', 'border-radius': '2px', 'margin-top': '24px'})
], className="mt-4")

if __name__ == "__main__":
    app.run_server(port=8765, debug=True)
