pip install vizro
pip install pandas
pip install dash
import dash
from dash import html, dcc, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Load the data (use your actual CSV path or DataFrame)
df = pd.read_csv('VizData.csv', encoding='latin-1')

# Create a Dash application with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout with Bootstrap components
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Data Analysis Dashboard", className="text-center my-4"), width=12),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Tabs(id="tabs", value='data_mart', children=[
                    dcc.Tab(label='Data Mart', value='data_mart', style={'fontWeight': 'bold'}),
                    dcc.Tab(label='Link Status', value='link_status', style={'fontWeight': 'bold'}),
                    dcc.Tab(label='Stored Procedures', value='stored_procs', style={'fontWeight': 'bold'}),
                    dcc.Tab(label='Database Schema', value='database_schema', style={'fontWeight': 'bold'}),
                ]),
                width=12
            ),
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='tabs-content'), width=12)
        ])
    ])
])

# Create callback to update tab content
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_tab_content(tab):
    if tab == 'data_mart':
        return html.Div([
            dash_table.DataTable(
                id='data_mart_table',
                columns=[
                    {'name': 'Data Mart', 'id': 'DATA MART'},
                    {'name': 'Report Name', 'id': 'REPORT NAME'},
                ],
                data=df[['DATA MART', 'REPORT NAME']].to_dict('records'),
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
            )
        ])
    elif tab == 'link_status':
        return html.Div([
            dash_table.DataTable(
                id='link_status_table',
                columns=[
                    {'name': 'Report Name', 'id': 'REPORT NAME'},
                    {'name': 'Link', 'id': 'LINK'},
                    {'name': 'Link Status', 'id': 'LINK STATUS'},
                ],
                data=df[['REPORT NAME', 'LINK', 'LINK STATUS']].to_dict('records'),
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
            )
        ])
    elif tab == 'stored_procs':
        return html.Div([
            dash_table.DataTable(
                id='stored_procs_table',
                columns=[
                    {'name': 'Report Name', 'id': 'REPORT NAME'},
                    {'name': 'Stored Procedure', 'id': 'SP'},
                ],
                data=df[['REPORT NAME', 'SP']].to_dict('records'),
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
            )
        ])
    elif tab == 'database_schema':
        return html.Div([
            dash_table.DataTable(
                id='database_schema_table',
                columns=[
                    {'name': 'Server', 'id': 'SERVER'},
                    {'name': 'Database', 'id': 'DB'},
                    {'name': 'Schema', 'id': 'SCHEMA'},
                    {'name': 'Table', 'id': 'TABLE'},
                ],
                data=df[['SERVER', 'DB', 'SCHEMA', 'TABLE']].to_dict('records'),
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
            )
        ])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
