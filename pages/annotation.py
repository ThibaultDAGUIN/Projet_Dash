import dash
from dash import html, dcc
from dash import dash_table
import json
import os

dash.register_page(__name__)

# Path to the annotations file
annotations_file = './data/annotations.json'

# Load annotations
def load_annotations():
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            return json.load(f)
    return []

# Prepare the data for the table
def prepare_table_data():
    annotations = load_annotations()
    table_data = []
    
    for annotation in annotations:
        table_data.append({
            'Image Name': annotation.get('id', 'N/A'),
            'Date': annotation.get('date', 'N/A'),
            'Annotateur': annotation.get('annotateur', 'Anonyme'),
            'Reviewer': annotation.get('reviewer', 'N/A')
        })
    
    return table_data

# Column setup for the DataTable
columns = [
    {'name': 'Image', 'id': 'Image Name'},
    {'name': 'Date', 'id': 'Date'},
    {'name': 'Annotateur', 'id': 'Annotateur'},
    {'name': 'Reviewer', 'id': 'Reviewer'}
]

# Layout of the page
layout = html.Div([
    html.H1("Liste des Annotations"),
    html.Div("Voici la liste des annotations effectuées :"),
    
    dash_table.DataTable(
        id='annotation-table',
        columns=columns,
        data=prepare_table_data(),
        style_table={'width': '80%', 'margin': 'auto'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={'textAlign': 'left'},
        page_size=10,  # Show 10 entries per page
    )
])