# -*- coding: utf-8 -*-

from dash import html, dash_table
import dash
import pandas as pd
from pathlib import Path

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/liste', name='Annotations', order=3)

# Charger les données
try:
    df = pd.read_csv('data/data_fictive_virg_utf8.csv', sep=";", encoding='utf-8')
    print("Colonnes disponibles dans le CSV:", df.columns)
except FileNotFoundError:
    print("Le fichier CSV n'a pas été trouvé. Assurez-vous qu'il est dans le dossier 'data'.")
    df = pd.DataFrame()

# Création du layout
layout = html.Div([
    html.H3("Liste des annotations", className="page-title"),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=15,  # Nombre de lignes par page
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            # style_data_conditional=[
            #     {
            #         'if': {'row_index': 'odd'},
            #         'backgroundColor': 'rgb(248, 248, 248)'
            #     }
            # ],
            style_data_conditional=[
                {
                    'if': {'filter_query': '{status-dropdown} = "In Progress"'},
                    'backgroundColor': 'yellow',
                    'color': 'black'
                },
                {
                    'if': {'filter_query': '{status-dropdown} = "New"'},
                    'backgroundColor': 'green',
                    'color': 'white'
                },
                {
                    'if': {'filter_query': '{status-dropdown} = ""'},
                    'backgroundColor': 'blue',
                    'color': 'white'
                }
            ],
            filter_action="native",  # Permet le filtrage des données
            sort_action="native",    # Permet le tri des données
            sort_mode="multi",       # Permet le tri sur plusieurs colonnes
            page_action="native",    # Pagination côté client
        )
    ], className="table-container")
], className="liste-container")

# CSS pour le style
app = dash.get_app()
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f2f5;
            }
            .liste-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .page-title {
                color: #333;
                text-align: center;
                margin-bottom: 20px;
            }
            .table-container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''