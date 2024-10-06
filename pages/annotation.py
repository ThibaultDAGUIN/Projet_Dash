import dash
from dash import html, dcc, dash_table, Input, Output, State
import json
import os
from datetime import datetime

dash.register_page(__name__)

annotations_file = './data/annotations.json'

def load_annotations():
    """Load annotations from the JSON file."""
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            return json.load(f)
    return []

def prepare_table_data():
    """Prepare data for the DataTable from annotations."""
    annotations = load_annotations()
    table_data = []
    
    for annotation in annotations:
        table_data.append({
            'Image Name': annotation.get('image_name', 'N/A'),
            'Date': annotation.get('date', 'N/A'),
            'Annotateur': annotation.get('annotateur', 'Anonyme'),
            'Reviewer': annotation.get('reviewer', 'N/A'),
            'Review Date': annotation.get('review_date', 'N/A'),
            'id': annotation.get('id')
        })
    
    # Sorting the data
    table_data.sort(key=lambda x: (x['Reviewer'] == 'N/A', x['Reviewer'], datetime.strptime(x['Date'], '%Y-%m-%d') if x['Date'] != 'N/A' else datetime.min))
    
    return table_data

columns = [
    {'name': 'Image Name', 'id': 'Image Name'},
    {'name': 'Date', 'id': 'Date'},
    {'name': 'Annotateur', 'id': 'Annotateur'},
    {'name': 'Reviewer', 'id': 'Reviewer'},
    {'name': 'Review Date', 'id': 'Review Date'},
    {'name': 'Verifier', 'id': 'Verifier', 'presentation': 'markdown'}
]

# Layout for the annotation page
layout = html.Div([
    html.H1("Liste des Annotations"),
    html.Div("Voici la liste des annotations effectuées :"),
    
    dash_table.DataTable(
        id='annotation-table',
        columns=columns,
        data=[
            {**row, 'Verifier': f'[Verifier](/verify?id={row["id"]})'}
            for row in prepare_table_data()
        ],
        style_table={'width': '80%', 'margin': 'auto'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        page_size=10,
    )
])

# Callback to update the table dynamically
@dash.callback(
    Output('annotation-table', 'data'),
    Input('annotation-table', 'data')  # Dummy input to trigger update on any change
)
def update_table(_):
    """Callback to update the DataTable with the latest annotation data."""
    return [
        {**row, 'Verifier': f'[Verifier](/verify?id={row["id"]})'}
        for row in prepare_table_data()
    ]
