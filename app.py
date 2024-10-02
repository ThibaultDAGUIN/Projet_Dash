import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"])

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dbc.NavbarSimple(
        children=[
            dbc.NavLink('Accueil', href='/accueil'),
            dbc.NavLink('Interface d\'annotation', href='/annoter'),
            dbc.NavLink('Liste des annotations', href='/annotation'),
            dbc.NavLink('Statistiques', href='/stats'),
            html.Span(id='user-text', className='ml-auto text-light align-self-center', style={'font-size': '0.9rem', 'marginLeft': '200px', 'marginRight':'0px'})

        ],
        brand="Projet d'Annotation M2VT",
        color="#333333",
        dark=True,
    ),

    dash.page_container,
    dcc.Store(id='user-name-store')  # Pour stocker le nom d'utilisateur en cours sur la session

])

@callback(
    Output('user-text', 'children'),
    Input('user-name-store', 'data')
)
def update_user_text(user_name):
    if user_name:
        return f"Vous êtes loggé en tant que {user_name}."
    return "Vous n'êtes pas loggé."

if __name__ == '__main__':
    app.run(debug=True)