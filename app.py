import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash('Open Data Analytics', external_stylesheets=[dbc.themes.BOOTSTRAP])

months_dict = {
    1: 'Janauary',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

df = pd.read_csv('data/db-cargo-delays-2016-deutschland.csv')

columns = ['Zugfahrten', 'Verspaetungsminuten', 'month']
grouped = df[columns].groupby(['month'])
months = grouped.groups.keys()

options = list(map(lambda x: {'label': months_dict[x], 'value': x}, grouped.groups.keys()))

row1 = dbc.Row(
    dbc.Col(
        html.H1('Homepage', style={'textAlign': 'center'}),
        md=12
    )
)
row2 = dbc.Row(
    dbc.Col(
        children=[
            dbc.InputGroup(
                children=[
                    dbc.InputGroupText("Months"),
                    dbc.Select(
                        id='select-months',
                        options=options,
                        value=2
                    ),
                ]
            ),
            dcc.Graph(id='scatter-plot-delays')
        ],
        md=5
    ),
    align="center"
)

container = dbc.Container(
    children=[row1, row2]
)

app.layout = container


@app.callback(
    Output('scatter-plot-delays', 'figure'),
    Input('select-months', 'value')
)
def update_plot(selected_month):
    val = int(selected_month)
    fig = px.scatter(data_frame=grouped.get_group(val),
                     x='Zugfahrten',
                     y='Verspaetungsminuten')
    fig.update_layout(title_text=months_dict[val], title_x=0.5)
    return fig


if __name__ == '__main__':
    print('Starting app server')
    app.run_server(debug=True)
