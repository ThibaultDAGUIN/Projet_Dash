from dash import html, dcc
import dash
import dash_bootstrap_components as dbc

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/apropos', name='A propos', order=5)

layout = html.Div(
    style={'margin': '20px'},
    children=[
        # Titre
        html.H1("À propos de nous", style={'text-align': 'center', 'margin-bottom': '30px'}),

        # Description de l'équipe
        html.H4("Qui sommes-nous ?", className="mt-4"),
        html.P(
            [
                "Quatre étudiants en 3ème année de ",
                html.A("BUT Science des Données", href="https://iutp.univ-poitiers.fr/sd/", className="text-primary"),
                " qui ont uni leurs forces pour réaliser ce projet, à l'occasion du cours de Dash dispensé par Clément GARCIN.",
            ],
            className="mb-4"
        ),

        # Présentation de l'équipe
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.A(
                                dbc.CardImg(src="https://static.wikia.nocookie.net/worldofcarsdrivein/images/1/1e/Chick_Hicks.png", top=True, style={"height": "150px", "object-fit": "contain"}),
                                href="https://www.linkedin.com/in/vadim-martin/",
                                target="_blank"
                            ),
                            dbc.CardBody(
                                [
                                    html.H5("Vadim MARTIN", className="card-title", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                    html.P("L'atout moustachu de l'annotation !", className="card-text", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                ]
                            )
                        ],
                        className="mb-2"  # Réduire la marge inférieure des cartes
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.A(
                                dbc.CardImg(src="https://static.wikia.nocookie.net/worldofcarsdrivein/images/9/96/The_king.png", top=True, style={"height": "150px", "object-fit": "contain"}),
                                href="https://www.linkedin.com/in/ma%C3%ABl-chaine-0996422a3/",
                                target="_blank"
                            ),
                            dbc.CardBody(
                                [
                                    html.H5("Maël CHAINE", className="card-title", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                    html.P("Le spécialiste musclé de la validation !", className="card-text", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                ]
                            )
                        ],
                        className="mb-2"  # Réduire la marge inférieure des cartes
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.A(
                                dbc.CardImg(src="https://static.wikia.nocookie.net/worldofcarsdrivein/images/d/dd/Doc_Hudson.png", top=True, style={"height": "150px", "object-fit": "contain"}),
                                href="https://fr.linkedin.com/in/daguint",
                                target="_blank"
                            ),
                            dbc.CardBody(
                                [
                                    html.H5("Thibault DAGUIN", className="card-title", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                    html.P("Le vieux sage des statistiques !", className="card-text", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                ]
                            )
                        ],
                        className="mb-2"  # Réduire la marge inférieure des cartes
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.A(
                                dbc.CardImg(src="https://static.wikia.nocookie.net/worldofcarsdrivein/images/7/79/Cars3sally.png", top=True, style={"height": "150px", "object-fit": "contain"}),
                                href="https://www.linkedin.com/in/manon-bonnaud-dubois-280266252/",
                                target="_blank"
                            ),
                            
                            dbc.CardBody(
                                [
                                    html.H5("Manon BONNAUD-DUBOIS", className="card-title", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                    html.P("L'habile débloqueuse de situations !", className="card-text", style={"white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"}),
                                ]
                            )
                        ],
                        className="mb-2"  # Réduire la marge inférieure des cartes
                    ),
                    width=3
                ),
            ],
            justify="center"
        ),

        # Exemple d'application
        html.H4("Le projet «Dash McQueen» : Un outil d'annotation d'images automobiles simple et performant", className="mt-2"),  # Réduire la marge supérieure du titre suivant
        html.P(
            """
            Notre application se concentre sur l'annotation d'images de voitures. L'objectif est d'identifier 
            précisément où se situe la voiture sur chaque image, afin de créer un ensemble de données annotées 
            qui pourra être utilisé pour entraîner des modèles de détection d'objets. Ces annotations permettront 
            d'améliorer la précision des modèles dans la reconnaissance de voitures sur d'autres images.
            """,
            className="mb-4"
        ),

        # Footer ou informations supplémentaires
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        html.Img(src="https://www.univ-poitiers.fr/wp-content/uploads/sites/10/2021/10/logo-up.svg", style={"margin": "10px"}, height="80px"),
                        href="https://www.univ-poitiers.fr"
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.A(
                        html.Img(src="https://iutp.univ-poitiers.fr/sd/wp-content/uploads/sites/137/2023/09/xLogo-SD-Niort-300x300.png.pagespeed.ic.pfiWeXH-r5.webp", style={"margin": "10px", "height": "80px"}),
                        href="https://iutp.univ-poitiers.fr/sd/"
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.A(
                        html.Img(src="https://www.dash-extensions.com/assets/dash_logo.png", style={"margin": "10px", "height": "80px"}),
                        href="https://www.dash-extensions.com/"
                    ),
                    width="auto"
                ),
            ],
            justify="center",
            className="mb-2"  # Utilisez une classe Bootstrap pour réduire la marge inférieure
        ),
    ]
)