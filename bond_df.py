from pyvalet import ValetInterpreter
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
vi = ValetInterpreter()

# Sample Data:
# BOC/V39055    Government of Canada benchmark bond yields - 10 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.10YR.DQ.YLD
# BOC/V39051    Government of Canada benchmark bond yields - 2 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.2YR.DQ.YLD
# BOC/V39052    Government of Canada benchmark bond yields - 3 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.3YR.DQ.YLD
# BOC/V39053    Government of Canada benchmark bond yields - 5 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.5YR.DQ.YLD
# BOC/V39054    Government of Canada benchmark bond yields - 7 year    daily https://www.bankofcanada.ca/valet/series/BD.CDN.7YR.DQ.YLD
# BOC/V39056    Government of Canada benchmark bond yields - long-term    daily https://www.bankofcanada.ca/valet/series/BD.CDN.LONG.DQ.YLD

links = [
         'BD.CDN.2YR.DQ.YLD',
         'BD.CDN.3YR.DQ.YLD',
         'BD.CDN.5YR.DQ.YLD',
         'BD.CDN.7YR.DQ.YLD',
         'BD.CDN.10YR.DQ.YLD',
         'BD.CDN.LONG.DQ.YLD']
bond_names = {
    'V39051': 'two year bond',
    'V39052': 'three year bond',
    'V39053': 'five year bond',
    'V39054': 'seven year bond',
    'V39055': 'ten year bond',
    'V39056': 'long term bond'
}
bond_names2 = {
    '2': 'two year bond',
    '3': 'three year bond',
    '5': 'five year bond',
    '7': 'seven year bond',
    '1': 'ten year bond',
    'L': 'long term bond'
}
# def fix_date(date):
#     if isinstance(date,str):
#         return date
#     date = date.to_pydatetime(date)
#     date = str(date)[:10]
#     return date

def get_df_helper(link):
    df_series, df = vi.get_series_observations(link, response_format='csv')
    df.columns = ['Date','Value','Bond type']
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df['Bond type'] = bond_names2[link[7]]
    return df

def get_df():
    frames = [get_df_helper(link) for link in links]
    df = pd.concat(frames)
    return df

def get_fig(df):
    return px.line(df)

def make_figure_table(df,value,start_date,end_date):
    if value:
        df = df[df['Bond type']==bond_names[value]]
    
    df = df.sort_index().loc[start_date:end_date]
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

