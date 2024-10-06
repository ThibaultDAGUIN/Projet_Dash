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
    {'name': 'Verifier', 'id': 'Verifier', 'presentation': 'markdown'}  # markdown for Verifier
    ]

# Layout for the annotation page
layout = html.Div([
    html.H1("Liste des Annotations"),
    html.Div("Voici la liste des annotations effectuées :"),
    
    dash_table.DataTable(
        id='annotation-table',
        columns=columns,
        data=[
            {**row, 'Verifier': f'<a href="/verify?id={row["id"]}">Vérifier</a>'}
            for row in prepare_table_data()
        ],
        style_table={'width': '80%', 'margin': 'auto'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        page_size=10,
    ),
    
    # Hidden Div for state or navigation
    html.Div(id='hidden-div', style={'display': 'none'}),
])

# Callback to update the table dynamically
@dash.callback(
    Output('annotation-table', 'data'),
    Input('annotation-table', 'data')  # Dummy input to trigger update on any change
)
def update_table(_):
    """Callback to update the DataTable with the latest annotation data."""
    return [
            {**row, 'Verifier': 'Cliquez la cellule pour vérifier'}
        for row in prepare_table_data()
    ]

# Callback to handle clicks on the Verifier links
@dash.callback(
    Output('hidden-div', 'children'),  # Using a hidden div to capture link clicks
    Input('annotation-table', 'active_cell')
)
def handle_verifier_click(active_cell):
    """Callback to handle clicks on the Verifier link."""
    if active_cell and active_cell['column_id'] == 'Verifier':
        row_index = active_cell['row']  # Get the row index of the clicked cell
        
        # Retrieve the full DataTable data
        data = prepare_table_data()  # You can also store this in a global variable if you want
        id_value = data[row_index]['id']  # Get the id from the corresponding row

        return dcc.Location(href=f'/verify?id={id_value}', id='redirect')
    return dash.no_update
