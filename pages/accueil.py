import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1("C'est la page de contexte"),
    html.Div("C'est la page de contexte"),
])