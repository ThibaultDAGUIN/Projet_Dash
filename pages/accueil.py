from dash import html, dcc
import dash
import dash_bootstrap_components as dbc

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/accueil', name='Accueil', order=1)

layout = html.Div(
    style={'margin': '20px'},
    children=[
        html.H1("Bienvenue dans notre application d'annotation", style={'text-align': 'center', 'margin-bottom': '40px'}),
        html.H2("Que souhaitez-vous faire ?", style={'text-align': 'center', 'margin-bottom': '40px'}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        [html.I(className="bi bi-pencil-square me-2"), "Annoter"],
                        href="/annoter",
                        color="primary",
                        className="btn-lg",
                        style={
                            'width': '200px', 'height': '200px', 'font-size': '24px',
                            'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                            'text-align': 'center'
                        }
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button(
                        [html.I(className="bi bi-check-circle me-2"), "Valider"],
                        href="/liste",
                        color="success",
                        className="btn-lg",
                        style={
                            'width': '200px', 'height': '200px', 'font-size': '24px',
                            'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                            'text-align': 'center'
                        }
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button(
                        [html.I(className="bi bi-bar-chart-line me-2"), "Mesurer"],
                        href="/stats",
                        color="danger",
                        className="btn-lg",
                        style={
                            'width': '200px', 'height': '200px', 'font-size': '24px',
                            'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                            'text-align': 'center',
                            'background-color': '#800000',  # Bordeaux
                            'border-color': '#800000'
                        }
                    ),
                    width="auto"
                ),
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(
                html.Footer(
                    dcc.Markdown(
                        """
                        **© 2024 Projet d'annotation - Dash**

                        Contributeurs du projet : Thibault DAGUIN, Vadim MARTIN, Maël CHAINE, Manon BONNAUD-DUBOIS
                        """
                    ),
                    className="text-center mt-5"
                )
            )
        )
    ]
)