# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# df = pd.read_csv('data/db-cargo-delays-2016-deutschland.csv')
# fig = px.bar(df, x="Zugfahrten", y="Verspaetungsminuten", color="weekofyear", barmode="group")

# fig = make_subplots(rows=3, cols=1)
#
# fig.append_trace(go.Scatter(
#    x = [3, 4, 5],
#    y = [1000, 1100, 1200],
# ), row = 1, col = 1)
#
# fig.append_trace(go.Scatter(
#    x = [2, 3, 4],
#    y = [100, 110, 120],
# ), row = 2, col = 1)
#
# fig.append_trace(go.Scatter(
#    x = [0, 1, 2],
#    y = [10, 11, 12]
# ), row = 3, col = 1)
#
# fig.update_layout(height = 600, width = 600, title_text = "Stacked Subplots")

df = pd.read_csv('data/db-cargo-delays-2016-deutschland.csv')

columns = ['Zugfahrten', 'Verspaetungsminuten', 'month']
grouped = df[columns].groupby(['month'])
months = grouped.groups.keys()

fig = px.scatter(data_frame=grouped.get_group(1), x='Zugfahrten', y='Verspaetungsminuten')

options = list(map(lambda x:  {'label': x, 'value': x}, grouped.groups.keys()))

app.layout = html.Div(children=[
    html.H1('Homepage', style={'textAlign': 'center'}),

    html.Div(children='Zugfahrten vs Verspaetungsminuten'),

    dcc.Dropdown(
        id='demo-dropdown',
        options=options,
        value=1
    ),
    html.Div(id='dd-output-container'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
   ],
    style={"width": "50%"},
)


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    print('Starting app server')
    app.run_server(debug=True)
