# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

df = pd.read_csv('data/db-cargo-delays-2016-deutschland.csv')
fig = px.bar(df, x="Zugfahrten", y="Verspaetungsminuten", color="weekofyear", barmode="group")

app.layout = html.Div(children=[
    html.H1('Hello Dash', style={'textAlign': 'center', 'color': '#7FDBFF'}),

    html.Div(children='''
        Plotly Dash - First Live Demo 2
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    print('Starting app server')
    app.run_server(debug=True)
