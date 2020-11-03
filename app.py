# Kelvin Du & Gordon Tang
###import stuffs###
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import re
from datetime import datetime as dt

import pandas as pd
from dash.dependencies import Input, Output
from bond_df import master_df,bond_names,fix_date

###Initialise stuff
app = dash.Dash(suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY])

###Initialise stuffs###
server = app.server
df = master_df
fig = px.line(df)
default_start_date = fix_date(df.index.min())
default_end_date = fix_date(df.index.max())
###Methods###
def make_figure_table(df,value,start_date,end_date):
    if value:
        df = df[df['Bond type']==bond_names[value]]

    df = df.loc[start_date:end_date]
    fig_table = go.Figure(
                    data= [go.Table(
                    header=dict(values=['Date','Values']),
                    cells=dict(values=[df.index.strftime("%d %b %Y"),df.Value]))],
              )
    fig_table.layout.paper_bgcolor = "#525252"
    fig_table.layout.title = {'font':{'color':"#fefffc"},'text':f"{bond_names[value] if value else 'All'} data numbers"}

    return fig_table

def make_graph(df,value,start_date,end_date):
    if value:
        df = df[df['Bond type']==bond_names[value]]

    df = df.pivot(columns='Bond type',values='Value')
    df = df.loc[start_date:end_date]

    fig = go.Figure()
    for col in df:
        fig.add_trace(go.Scatter(x=list(df.index),y=list(df[col]),name=col))

    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))
    fig.layout.paper_bgcolor = "#525252"
    fig.layout.yaxis = {'title':{'text':'Value($)'},'color':'#fefffc'}
    fig.layout.xaxis.tickfont = {'color':'#fefffc'}
    fig.layout.legend = {'bgcolor':'#525252','font':{'color':'#fefffc'}}
    fig.layout.title = {'font':{'color':"#fefffc"},'text':f"{bond_names[value] if value else 'All'} daily bond yield"}

    return fig


def get_marks(df):
    dates = df.index.strftime("%b %Y").unique()
    marks = {}
    for i in range(dates.size):
        marks[i] = dates[i]
    return marks



###Initialise stuff###
time_range = get_marks(df)
fig_table = make_figure_table(df,"",default_start_date,default_end_date)
fig_graph = make_graph(df, "",default_start_date,default_end_date)


navbar = dbc.Navbar([
        dbc.Row([
                dbc.Col(html.Figure(html.Span([html.Span(className = 'bottom'),
                                                html.Span(className = 'top')],
                                                className = 'letter n')),
                                                className = 'letter-wrapper'),
                dbc.Col(dbc.NavLink("Home", href="#",style=dict(color='#ffffff'))),
                    dbc.Col(dbc.NavLink(" ", href="/page-1",style=dict(color='#ffffff'))),
                    dbc.Col(dbc.NavLink(" ", href="/page-2",style=dict(color='#ffffff')))
                # dbc.Col(dbc.NavLink("Go to Page 1", href="/page-1",style=dict(color='#ffffff'))),
                # dbc.Col(dbc.NavLink("Go to Page 2", href="/page-2",style=dict(color='#ffffff')))
                ]),
        dbc.Row([
                dbc.Col(dbc.Input(type="search", placeholder="Search")),
                dbc.Col(dbc.Button("Search", color="primary", className="ml-2"),width="auto")
                ],
                no_gutters=True,
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                align="center")],
        color="#313131",
        sticky="top")

###layout stuff###
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
        placeholder='Select time period',
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

###layout stuff###
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

###callback stuff###
#change
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

#change
@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


#change
# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return home_page_layout
    # You could also return a 404 "URL not found" page here

@app.callback(
    Output('output-dropdown-container', 'children'),
    [Input(component_id='dropdown', component_property='value')])
def update_selection_view(value):
    if value:
        return f'You have selected to view the {bond_names[value]}'
    else:
        return 'You have not selected a bond type'

@app.callback([
    Output('myield-graph', 'figure'),
    Output('table','figure')
], [Input(component_id='dropdown', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_graph_and_table(value,start_date, end_date):
    start_date = fix_date(start_date)
    end_date = fix_date(end_date)
    fig_table = make_figure_table(df, value,start_date,end_date)
    fig_graph = make_graph(df, value,start_date,end_date)
    return fig_graph, fig_table

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    #update fig table and fig graph

    start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    start_date = start_date.strftime('%B %d, %Y')

    end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
    end_date = end_date.strftime('%B %d, %Y')

    return f'you have selected to view bond yields betwen {start_date} and {end_date}'

if __name__ == '__main__':
    app.run_server(debug=True)
