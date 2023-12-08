from dash import Dash, dcc, html, Input, Output
from bond_df import get_df, get_fig, bond_names, make_figure_table, make_graph, get_marks
import dash_bootstrap_components as dbc
from datetime import datetime as dt
import re

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

###INITIALIZE###
app = Dash(suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY])
server = app.server
df = get_df()
fig = get_fig(df)
default_start_date = df.index.min().strftime("%Y-%m-%d")
default_end_date = df.index.max().strftime("%Y-%m-%d")
time_range = get_marks(df)
fig_table = make_figure_table(df,"",default_start_date,default_end_date)
fig_graph = make_graph(df, "",default_start_date,default_end_date)

###DEFINE PAGE LAYOUT###
navbar = dbc.Navbar([
    html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    ],
                ),
                href="https://plot.ly",
            ),
        dbc.Row([
                dbc.Col(dbc.NavLink("Home", href="#",style=dict(color='#ffffff'))),
                    dbc.Col(dbc.NavLink(" ", href="/page-1",style=dict(color='#ffffff'))),
                    dbc.Col(dbc.NavLink(" ", href="/page-2",style=dict(color='#ffffff')))
                ]),
        dbc.Row([
                dbc.Col(dbc.Input(type="search", placeholder="Search")),
                dbc.Col(dbc.Button("Search", color="primary", className="ml-2"),width="auto")
                ],
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                align="center")],
        color="#313131",
        sticky="top")

home_page_layout = html.Div([
    navbar,
    dcc.Dropdown(
        id="dropdown",

        options=[
            {'label': 'two year bond', 'value': 'V39051'},
            {'label': 'three year bond', 'value': 'V39052'},
            {'label': 'five year bond', 'value': 'V39053'},
            {'label': 'seven year bond', 'value': 'V39054'},
            {'label': 'ten year bond', 'value': 'V39055'},
            {'label': 'long term bond', 'value': 'V39056'},
        ],
        placeholder='Select Bond Type',
        value= ""),
    html.Div(id='output-dropdown-container'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=df.index.min(),
        max_date_allowed=df.index.max(),
        start_date=df.index.min(),
        end_date=df.index.max()
    ),
    html.Div(id='output-container-date-picker-range'),

    html.Div(id='dd-output-container'),
        html.Div([
            html.Div([
                dcc.Graph(id='myield-graph', figure=fig)]),
            html.Div([
                dcc.Graph(id='table',figure=fig_table)])
        ],style={'columnCount':2}),
],style={'backgroundColor':'#13d0a7'})

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

###DEFINE CALLBACKS###

#page_1_dropdown
@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

#page_2_radios
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return home_page_layout
    # You could also return a 404 "URL not found" page here

#update_selection_view
@app.callback(
    Output('output-dropdown-container', 'children'),
    [Input(component_id='dropdown', component_property='value')])
def update_selection_view(value):
    if value:
        return f'You have selected to view the {bond_names[value]}'
    else:
        return 'You have not selected a bond type'

#update_graph_and_table
@app.callback([
    Output('myield-graph', 'figure'),
    Output('table','figure')
], [Input(component_id='dropdown', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_graph_and_table(value,start_date, end_date):
    fig_table = make_figure_table(df, value,start_date,end_date)
    fig_graph = make_graph(df, value,start_date,end_date)
    return fig_graph, fig_table

#update fig table and fig graph
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    start_date = start_date.strftime('%B %d, %Y')

    end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
    end_date = end_date.strftime('%B %d, %Y')

    return f'you have selected to view bond yields betwen {start_date} and {end_date}'

if __name__ == '__main__':
    app.run_server(debug=True)
