import dash
from dash import html, dcc, dash_table, Input, Output, State
import json
import os
from datetime import datetime

dash.register_page(__name__)

annotations_file = './data/annotations.json'

def load_annotations():
    """Charger les annotations à partir du fichier JSON."""
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            return json.load(f)
    return []

def prepare_table_data():
    """Préparer les données pour le DataTable à partir des annotations."""
    annotations = load_annotations()
    table_data = []
    
    for annotation in annotations:
        table_data.append({
            'Nom Image': annotation.get('nom_image', 'N/A'),
            'Date': annotation.get('date_annotation', 'N/A'),
            'Annotateur': annotation.get('annotateur', 'Anonyme'),
            'Reviewer': annotation.get('reviewer', 'N/A'),
            'Date Review': annotation.get('date_review', 'N/A'),
            'id': annotation.get('id')
        })
    
    # Tri des données
    table_data.sort(key=lambda x: (x['Reviewer'] == 'N/A', x['Reviewer'], datetime.strptime(x['Date'], '%Y-%m-%d') if x['Date'] != 'N/A' else datetime.min))
    
    return table_data

columns = [
    {'name': 'Nom Image', 'id': 'Image Name'},
    {'name': 'Date', 'id': 'Date'},
    {'name': 'Annotateur', 'id': 'Annotateur'},
    {'name': 'Reviewer', 'id': 'Reviewer'},
    {'name': 'Date Review', 'id': 'Review Date'},
    {'name': 'Verifier', 'id': 'Verifier', 'presentation': 'markdown'}  # markdown pour Verifier
]

# Mise en page pour la page d'annotations
layout = html.Div([
    html.H1("Liste des Annotations", className='text-center my-3'),
    html.Div("Voici la liste des annotations effectuées :", className='text-center my-3'),
    
    dash_table.DataTable(
        id='annotation-table',
        columns=columns,
        data=[
            {**row, 'Verifier': f'<a href="/verifier?id={row["id"]}">Vérifier</a>'}
            for row in prepare_table_data()
        ],
        style_table={'width': '80%', 'margin': 'auto'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        page_size=10,
    ),
    
    # Div cachée pour l'état ou la navigation
    html.Div(id='hidden-div', style={'display': 'none'}),
])

# Callback pour mettre à jour le tableau dynamiquement
@dash.callback(
    Output('annotation-table', 'data'),
    Input('annotation-table', 'data')  # Entrée factice pour déclencher la mise à jour à chaque changement
)
def update_table(_):
    """Callback pour mettre à jour le DataTable avec les dernières données d'annotation."""
    return [
            {**row, 'Verifier': 'Cliquez la cellule pour vérifier l\'annotation'}
        for row in prepare_table_data()
    ]

# Callback pour gérer les clics sur les liens Verifier
@dash.callback(
    Output('hidden-div', 'children'),  # Utilisation d'une div cachée pour capturer les clics sur le lien
    Input('annotation-table', 'active_cell')
)
def handle_verifier_click(active_cell):
    """Callback pour gérer les clics sur le lien Verifier."""
    if active_cell and active_cell['column_id'] == 'Verifier':
        row_index = active_cell['row']  # Obtenir l'index de la ligne de la cellule cliquée
        
        # Récupérer les données complètes du DataTable
        data = prepare_table_data()  # Vous pouvez aussi stocker ceci dans une variable globale si nécessaire
        id_value = data[row_index]['id']  # Obtenir l'id de la ligne correspondante

        return dcc.Location(href=f'/verifier?id={id_value}', id='redirect')
    return dash.no_update
