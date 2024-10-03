# import dash
# from dash import dcc, html, Input, Output, callback, State
# from skimage import io
# import plotly_express as px
# import os, json, base64, uuid
# import dash_bootstrap_components as dbc
# from urllib.parse import parse_qs, urlparse

# # Dossier images et fichiers JSON
# dossier_img = './data/cars/'
# annotations_file = './data/annotations.json'

# dash.register_page(__name__)

# # Function to get the image name from the URL parameters
# def get_image_name_from_url():
#     parsed_url = urlparse(dash.callback_context.request.url)
#     query_params = parse_qs(parsed_url.query)
#     return query_params.get('image_name', [None])[0]

# image_name = get_image_name_from_url()

# # Load the image for annotation if the image_name exists
# if image_name:
#     img_path = os.path.join(dossier_img, image_name)
#     if os.path.exists(img_path):
#         img = io.imread(img_path)
#         fig = px.imshow(img)
#         fig.update_layout(
#             dragmode="drawrect",
#             newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
#         )
#     else:
#         img = None
#         fig = None
# else:
#     img = None
#     fig = None

# layout = html.Div(
#     [
#         html.H3(f"Annotating Image: {image_name}" if image_name else "No Image Selected"),
#         dcc.Graph(id="graph-styled-annotations", figure=fig),

#         dcc.Upload(
#             id="import-image",
#             children=html.Div(
#                 ['Glissez et déposez une image ici, ou ',
#                  html.A('sélectionnez une image')],
#                 style={
#                     'borderWidth': '0.5px', 'borderStyle': 'solid', 'backgroundColor': 'rgba(66, 66, 66, 0.15)',
#                     'padding': '20px', 'textAlign': 'center', 'width': '50%',
#                     'margin': '5px auto', 'cursor': 'pointer'
#                 }
#             ),
#             multiple=False
#         ),

#         dbc.Button(
#             "Valider l'annotation",
#             id="bouton_valider",
#             color='success',
#             n_clicks=0,
#             className='my-3'
#         ),

#         # Additional UI components as needed...
#     ]
# )

# # Callbacks for handling the image upload, annotation, etc. can be added here...
