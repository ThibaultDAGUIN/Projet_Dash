# annotation.py
import dash
from dash import html, dcc, dash_table, Input, Output, State
import json
import os

dash.register_page(__name__)

annotations_file = './data/annotations.json'

def load_annotations():
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            return json.load(f)
    return []

def prepare_table_data():
    annotations = load_annotations()
    table_data = []
    for annotation in annotations:
        table_data.append({
            'Image Name': annotation.get('image_name', 'N/A'),
            'Date': annotation.get('date', 'N/A'),
            'Annotateur': annotation.get('annotateur', 'Anonyme'),
            'Reviewer': annotation.get('reviewer', 'N/A'),
            'id': annotation.get('id')  # Pass ID for Verifier button
        })
    return table_data

columns = [
    {'name': 'Image Name', 'id': 'Image Name'},
    {'name': 'Date', 'id': 'Date'},
    {'name': 'Annotateur', 'id': 'Annotateur'},
    {'name': 'Reviewer', 'id': 'Reviewer'},
    {'name': 'Verifier', 'id': 'Verifier', 'presentation': 'markdown'}
]

layout = html.Div([
    html.H1("Liste des Annotations"),
    html.Div("Voici la liste des annotations effectuées :"),
    
    dash_table.DataTable(
        id='annotation-table',
        columns=columns,
        data=[
            {**row, 'Verifier': f'[Verifier](/verify?id={row["id"]})'}  # Create link for Verifier button
            for row in prepare_table_data()
        ],
        style_table={'width': '80%', 'margin': 'auto'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        page_size=10,
    )
])
