import dash
from dash import html, dcc, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data from the CSV files
fla_df = pd.read_csv('FLA.csv')
flb_df = pd.read_csv('FLB.csv')
flc_df = pd.read_csv('FLC.csv')
fld_df = pd.read_csv('FLD.csv')

# Extract unique values for database options
db_options = [{'label': db, 'value': db} for db in flb_df['DB'].dropna().unique() if db]

# Define fixed schema options
schema_options = [
    {'label': 'dbo', 'value': 'dbo'},
    {'label': 'mer', 'value': 'mer'},
    {'label': 'AADUtilUser', 'value': 'AADUtilUser'}
]

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    dbc.Container([
        # Title
        dbc.Row([
            dbc.Col(html.H1("WSS SSRS CATALOG", className="text-center my-4"), width=12),
        ]),
        # Dropdown filters
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='data_mart_selector',
                    options=[{'label': mart, 'value': mart} for mart in fld_df['DATA MART'].unique()],
                    placeholder="Select Data Mart",
                    multi=True,
                    style={'width': '100%'}
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='schema_slicer',
                    options=schema_options,
                    placeholder="Select Schema",
                    multi=True,
                    style={'width': '100%'}
                ),
                width=4
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='db_slicer',
                    options=db_options,
                    placeholder="Select Database",
                    multi=True,
                    style={'width': '100%'}
                ),
                width=4
            ),
        ], className="mt-4"),
        # Report selector
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='report_selector',
                    placeholder="Select Report",
                    multi=True,
                    style={'width': '100%'}
                ),
                width=12
            ),
        ], className="mt-4"),
        # Tabs for different content
        dbc.Row([
            dbc.Col(dcc.Tabs(id="tabs", value='report_links', children=[
                dcc.Tab(label='Report Links', value='report_links'),
                dcc.Tab(label='Database Schema', value='database_schema'),
                dcc.Tab(label='Stored Procedures', value='stored_procs'),
                dcc.Tab(label='Data Mart Histogram', value='data_mart_histogram'),
            ]), width=12),
        ]),
        # Placeholder for tab content
        dbc.Row([
            dbc.Col(html.Div(id='tabs-content'), width=12)
        ]),
    ])
])

# Callbacks to update report selector and tab content
@app.callback(
    Output('report_selector', 'options'),
    [Input('data_mart_selector', 'value'),
     Input('schema_slicer', 'value'),
     Input('db_slicer', 'value')]
)
def update_report_selector(selected_marts, selected_schemas, selected_dbs):
    filtered_reports = fld_df
    if selected_marts:
        filtered_reports = filtered_reports[filtered_reports['DATA MART'].isin(selected_marts)]
    if selected_schemas:
        filtered_reports = filtered_reports[
            filtered_reports['REPORT NAME'].isin(
                flb_df[flb_df['SCHEMA'].isin(selected_schemas)]['TABLE']
            )
        ]
    if selected_dbs:
        filtered_reports = filtered_reports[
            filtered_reports['REPORT NAME'].isin(
                flb_df[flb_df['DB'].isin(selected_dbs)]['TABLE']
            )
        ]
    return [{'label': report, 'value': report} for report in filtered_reports['REPORT NAME'].unique()]

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('data_mart_selector', 'value'),
     Input('schema_slicer', 'value'),
     Input('db_slicer', 'value'),
     Input('report_selector', 'value')]
)
def render_tab_content(tab, selected_marts, selected_schemas, selected_dbs, selected_reports):
    if tab == 'report_links':
        filtered_fla_df = fla_df
        if selected_reports:
            filtered_fla_df = filtered_fla_df[filtered_fla_df['REPORT NAME'].isin(selected_reports)]
        return dash_table.DataTable(
            data=filtered_fla_df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in fla_df.columns],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
        )
    elif tab == 'database_schema':
        filtered_flb_df = flb_df
        if selected_schemas:
            filtered_flb_df = filtered_flb_df[filtered_flb_df['SCHEMA'].isin(selected_schemas)]
        if selected_dbs:
            filtered_flb_df = filtered_flb_df[filtered_flb_df['DB'].isin(selected_dbs)]
        return dash_table.DataTable(
            data=filtered_flb_df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in flb_df.columns],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
        )
    elif tab == 'stored_procs':
        filtered_flc_df = flc_df
        if selected_reports:
            filtered_flc_df = filtered_flc_df[filtered_flc_df['REPORT NAME'].isin(selected_reports)]
        return dash_table.DataTable(
            data=filtered_flc_df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in flc_df.columns],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}
        )
    elif tab == 'data_mart_histogram':
        filtered_flb_df = flb_df
        if selected_schemas:
            filtered_flb_df = filtered_flb_df[filtered_flb_df['SCHEMA'].isin(selected_schemas)]
        if selected_dbs:
            filtered_flb_df = filtered_flb_df[filtered_flb_df['DB'].isin(selected_dbs)]

        data_mart_counts = fld_df['DATA MART'].value_counts().reset_index()
        data_mart_counts.columns = ['DATA MART', 'Count']

        fig_data_mart = px.histogram(data_mart_counts, x='DATA MART', y='Count',
                                     title='Data Mart Histogram',
                                     labels={'DATA MART': 'Data Mart', 'Count': 'Count of Reports'})

        return dcc.Graph(figure=fig_data_mart)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
