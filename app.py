import dash
from dash import html, dcc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import flask
import time
from datetime import datetime, date, timedelta
import requests
import csv
import io
import pandas as pd
import numpy as np
from datetime import datetime as dt


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

today = time.strftime("%Y-%m-%d")
print(today)
today2 = datetime.now()
year = datetime.now().year
f_date = datetime(year, 1, 1)
delta = today2 - f_date
days = delta.days

capacities = {'Lake Powell Glen Canyon Dam and Powerplant': 24322000, 'Lake Mead Hoover Dam and Powerplant': 26134000, 'FLAMING GORGE RESERVOIR': 3788700, 'NAVAJO RESERVOIR': 1708600, 'BLUE MESA RESERVOIR': 940800, 'Powell Mead Combo': 50456000, 'UR': 6438100}

powell_data_url= 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=' + today + '&after=1999-12-29&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20'

mead_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=6124&before=' + today + '&after=1999-12-30&filename=Lake%20Mead%20Hoover%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1937-05-28%20-%202020-11-30)&order=ASC'

blue_mesa_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=76&before=' + today + '&after=1999-12-30&filename=Blue%20Mesa%20Reservoir%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(2000-01-01%20-%202021-07-14)&order=ASC'

navajo_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=613&before=' + today + '&after=1999-12-30&filename=Navajo%20Reservoir%20and%20Dam%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1999-12-31%20-%202021-07-14)&order=ASC'

fg_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=337&before=' + today + '&after=1999-12-30&filename=Flaming%20Gorge%20Reservoir%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1999-12-31%20-%202021-07-15)&order=ASC'

# drought_data_url = 'https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=08&startdate=1/1/2000&enddate=' + today + '&statisticsType=2'

# https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=08&startdate=1/1/2000&enddate=2021/9/28&statisticsType=2

@app.callback(
    Output('powell-water-data-raw', 'data'),
    Input('interval-component', 'n_intervals'))
def get_powell_data(n):
    powell_data_raw = pd.read_csv(powell_data_url)
    # print(powell_data_raw)
    return powell_data_raw.to_json()

@app.callback(
    Output('mead-water-data-raw', 'data'),
    Input('interval-component', 'n_intervals'))
def get_mead_data(n):
    mead_data_raw = pd.read_csv(mead_data_url)
    # print(powell_data_raw)
    return mead_data_raw.to_json()

# @app.callback(
#     Output('drought-data-raw', 'data'),
#     Input('interval-component', 'n_intervals'))
# def get_drought_data(n):
#     df = pd.read_csv(drought_data_url)
#     # df = pd.read_json(io.StringIO(drought_data_url.decode('utf-8')))
#     df.drop(['StatisticFormatID', 'StateAbbreviation', 'MapDate'] , axis=1, inplace=True)
#     df.set_index('date', inplace=True)
#     print(df)
#     df['DSCI'] = (df['D0'] + (df['D1']*2) + (df['D2']*3) + (df['D3']*4 + (df['D4']*5)))
#     df = df.sort_index(ascending=True)
#     df['MA'] = df['DSCI'].rolling(window=10).mean()
#     return df.to_json()
@app.callback(
    Output('drought-data', 'data'),
    Input('interval-component', 'n_intervals'))
def data(n):
    url = 'https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=08&startdate=1/1/2000&enddate=' + today + '&statisticsType=2'

    # combo_data = pd.read_json(com)
    # print(combo_data)
    r = requests.get(url).content

    df = pd.read_json(io.StringIO(r.decode('utf-8')))
    # print(df)

    df['date'] = pd.to_datetime(df['MapDate'].astype(str), format='%Y%m%d')

    df.drop(['StatisticFormatID', 'StateAbbreviation', 'MapDate'] , axis=1, inplace=True)
    df.set_index('date', inplace=True)
    # print(df)
    df['DSCI'] = (df['D0'] + (df['D1']*2) + (df['D2']*3) + (df['D3']*4 + (df['D4']*5)))
    # print(df)
    return df.to_json()


# powell_data_raw = pd.read_csv(powell_data_url)
# mead_data_raw = pd.read_csv(mead_data_url)
blue_mesa_data_raw = pd.read_csv(blue_mesa_data_url)
navajo_data_raw = pd.read_csv(navajo_data_url)
fg_data_raw = pd.read_csv(fg_data_url)
# drought_data_raw = pd.read_csv(drought_data_url)
# print(blue_mesa_data_raw)
# print(drought_data_raw)
def get_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H2(
                'Colorado River Water Storage',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])

    return header

def get_emptyrow(h='15px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

def get_navbar(p = 'homepage'):
    navbar_homepage = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Upper Reservoirs'),
                href='/ur'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Drought'),
                href='/drought'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2'),
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    non_home = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    if p == 'homepage':
        return navbar_homepage
    else:
        return non_home

homepage = html.Div([
    get_header(),
    get_navbar('homepage'),
    get_emptyrow(),
    html.Div([
        html.Div([
            dcc.Loading(
            id="loading-powell",
            type="default",
            children=html.Div(dcc.Graph(id='powell-levels'))),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Loading(
            id="loading-mead",
            type="default",
            children=html.Div(dcc.Graph(id='mead-levels'))),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Loading(
            id="loading-combo",
            type="default",
            children=html.Div(dcc.Graph(id='combo-levels'))),
        ],
            className='four columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H6('Current Storage - AF', style={'text-align': 'center'})
        ],
            className='three columns'
        ),
        html.Div([
            html.H6('Pct. Full', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('24 hr', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('C.Y.', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Year', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Rec Low', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Diff', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Rec Low Date', style={'text-align': 'center'})
        ],
            className='two columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div(id='cur-levels')
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='powell-annual-changes'
            )
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(
                id='mead-annual-changes'
            )
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(
                id='combo-annual-changes'
            )
        ],
            className='four columns'
        ),
        
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            dcc.Link(
                html.H6(children='Powell Data'),
                href='/apps/powell'
            )
        ],
            className='four columns',
            style={'text-align': 'center'}
        ),
    ],
        className='row'
    ),
    dcc.Interval(
        id='interval-component',
        interval=500*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Store(id='powell-water-data'),
    dcc.Store(id='powell-water-data-raw'),
    dcc.Store(id='mead-water-data'),
    dcc.Store(id='mead-water-data-raw'),
    dcc.Store(id='combo-water-data'),
    dcc.Store(id='powell-annual-change'),
    dcc.Store(id='mead-annual-change'),
    dcc.Store(id='combo-annual-change'),
])

layout_ur = html.Div([
    get_header(),
    get_navbar('non-home'),
    get_emptyrow(),
    html.Div([
        html.Div([
            dcc.Graph(
                id='bm-levels',
            ),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(
                id='navajo-levels',
            ),
        ],
            className='four columns'
        ),
        html.Div([
            dcc.Graph(
                id='fg-levels',
            ),
        ],
            className='four columns'
        ),

    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H6('Current Storage - AF', style={'text-align': 'center'})
        ],
            className='three columns'
        ),
        html.Div([
            html.H6('Pct. Full', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('24 hr', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('C.Y.', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Year', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Rec Low', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Diff', style={'text-align': 'center'})
        ],
            className='one column'
        ),
        html.Div([
            html.H6('Rec Low Date', style={'text-align': 'center'})
        ],
            className='two columns'
        ),
    ],
    className='row'
    ),
    html.Div([
        html.Div(id='upper-cur-levels')
    ],
        className='row'
    ),
    dcc.Interval(
        id='interval-component',
        interval=500*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Store(id='blue-mesa-water-data'),
    dcc.Store(id='navajo-water-data'),
    dcc.Store(id='fg-water-data'),
    dcc.Store(id='ur-water-data'),

])

layout_drought = html.Div([
    get_header(),
    get_navbar('non-home'),
    get_emptyrow(),
    html.Div([
        html.H2(
            'Drought',
            className='twelve columns',
            style={'text-align': 'center'}
        )
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='drought-graph'
            )
        ],
            className='eight columns'
        ), 
        html.Div([
            dcc.Markdown('''Moving Avg in Weeks'''),
            daq.NumericInput(
                id='MA-input',
                value=0
            ),
        ],
            className='one column'
        ),
    ],  
        className='row'
    ),
    get_emptyrow(),
    html.Div([
        html.Div([
            dcc.Graph(
                id='dsci-graph'
            )
        ],
            className='eight columns'
        ), 
    ],  
        className='row'
    ),
    # get_emptyrow(),
    html.Div([
        html.Div([
            dcc.Graph(
                id='diff-graph'
            )
        ],
            className='eight columns'
        ), 
    ],  
        className='row'
    ),
    dcc.Interval(
        id='interval-component',
        interval=500*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Store(id='drought-data'),
    dcc.Store(id='combo-water-data'),
    dcc.Store(id='combo-annual-change'),
])

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# homepage = html.Div([
#     home_page_App(),
#     # dcc.Link('Upper Reservoirs"', href='/page-1'),
#     # html.Br(),
#     # dcc.Link('Navigate to "/page-2"', href='/page-2'),
# ])

# layout_ur = html.Div([
#     get_header(),
    # ur_App(),
    # dcc.Input(id='input-1-state', type='text', value='Montreal'),
    # dcc.Input(id='input-2-state', type='text', value='Canada'),
    # html.Button(id='submit-button', n_clicks=0, children='Submit'),
    # html.Div(id='output-state'),
    # html.Br(),
    # dcc.Link('Navigate to "/"', href='/'),
    # html.Br(),
    # dcc.Link('Navigate to "/page-2"', href='/page-2'),
# ])

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    homepage,
    layout_ur,
    layout_drought,
])

# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return homepage
    elif pathname == "/ur":
        return layout_ur
    elif pathname == "/drought":
        return layout_drought
    else:
        return homepage

# Page 1 callbacks
@app.callback(Output('output-state', 'children'),
              Input('submit-button', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    return ('The Button has been pressed {} times,'
            'Input 1 is "{}",'
            'and Input 2 is "{}"').format(n_clicks, input1, input2)

########## DATA CALLBACKS ########################################

########## POWELL MEAD DATA ######################################

@app.callback([
    Output('powell-water-data', 'data'),
    Output('mead-water-data', 'data'),
    Output('combo-water-data', 'data')],
    [Input('interval-component', 'n_intervals'),
    Input('powell-water-data-raw', 'data'),
    Input('mead-water-data-raw', 'data')])
def clean_powell_data(n, powell_data_raw, mead_data_raw):
    df_powell_water = pd.read_json(powell_data_raw)
    # print(df_powell_water)
    df_powell_water = df_powell_water.drop(df_powell_water.columns[[1,3,4,5,7,8]], axis=1)
    
    df_powell_water.columns = ["Site", "Water Level", "Date"]
    
    df_powell_water = df_powell_water[10:]
    
    df_powell_water['power level'] = 6124000
    df_powell_water['sick pool'] = 4158000
    df_powell_water['dead pool'] = 1895000
   
    df_powell_water = df_powell_water.set_index("Date")
    df_powell_water = df_powell_water.sort_index()
       

    df_mead_water = pd.read_json(mead_data_raw)
    df_mead_water = df_mead_water.drop(df_mead_water.columns[[1,3,4,5,7,8]], axis=1)
    df_mead_water.columns = ["Site", "Water Level", "Date"]
    df_mead_water = df_mead_water[7:]
    
    df_mead_water['1090'] = 10857000
    df_mead_water['1075'] = 9601000
    df_mead_water['1050'] = 7683000
    df_mead_water['1025'] = 5981000
    df_mead_water['Dead Pool'] = 2547000

    df_mead_water = df_mead_water.set_index("Date")
    df_mead_water = df_mead_water.sort_index(ascending=True)
    # print(df_mead_water)
    
    powell_df = df_powell_water.drop(df_powell_water.index[0])
    mead_df = df_mead_water.drop(df_mead_water.index[0])

    start_date = date(1963, 6, 29)
    date_now = date.today()
    delta = date_now - start_date
    
    days = delta.days
    df_mead_water = mead_df[9527:]
    
    df_total = pd.merge(mead_df, powell_df, how='inner', left_index=True, right_index=True)
  
    df_total.rename(columns={'Date_x':'Date'}, inplace=True)
    
    df_total['Value_x'] = df_total['Water Level_x'].astype(int)
    df_total['Value_y'] = df_total['Water Level_y'].astype(int)
    df_total['Water Level'] = df_total['Value_x'] + df_total['Value_y']
    
    # combo_df = df_total.drop(df_total.index[0])
    combo_df = df_total
    # print(combo_df)

    return powell_df.to_json(), mead_df.to_json(), combo_df.to_json()

###################### UPPER RES DATA ################

@app.callback([
    Output('blue-mesa-water-data', 'data'),
    Output('navajo-water-data', 'data'),
    Output('fg-water-data', 'data'),
    Output('ur-water-data', 'data')],
    Input('interval-component', 'n_intervals'))
def clean_powell_data(n):
    bm_df = blue_mesa_data_raw
    nav_df = navajo_data_raw
    fg_df = fg_data_raw
    # print(bm_df)

    df_bm_water = bm_df.drop(bm_df.columns[[1,3,4,5,7,8]], axis=1)
    # print(df_nav_water)
    df_bm_water.columns = ["Site", "Value", "Date"]

    df_bm_water = df_bm_water[9:]
    

    df_bm_water = df_bm_water.set_index("Date")
    df_bm_water = df_bm_water.sort_index()
    
    df_nav_water = nav_df.drop(nav_df.columns[[1,3,4,5,7,8]], axis=1)
    

    df_nav_water.columns = ["Site", "Value", "Date"]

    df_nav_water = df_nav_water[7:]
    

    df_nav_water = df_nav_water.set_index("Date")
    df_nav_water = df_nav_water.sort_index()
   
    df_fg_water = fg_df.drop(fg_df.columns[[1,3,4,5,7,8]], axis=1)
    df_fg_water.columns = ["Site", "Value", "Date"]

    df_fg_water = df_fg_water[7:]
    

    df_fg_water = df_fg_water.set_index("Date")
    df_fg_water = df_fg_water.sort_index()

    blue_mesa_df = df_bm_water.drop(df_bm_water.index[0])
    navajo_df = df_nav_water.drop(df_nav_water.index[0])
    fg_df = df_fg_water.drop(df_fg_water.index[0])

    ur_total = pd.merge(blue_mesa_df, navajo_df, how='inner', left_index=True, right_index=True)

    ur_total = pd.merge(ur_total, fg_df, how='inner', left_index=True, right_index=True)
    # print(ur_total)
    # ur_total['Water Level'] = ur_total[]

    return blue_mesa_df.to_json(), navajo_df.to_json(), fg_df.to_json(), ur_total.to_json()


#################### GRAPH CALLBACKS ################################

@app.callback([
    Output('powell-levels', 'figure'),
    Output('mead-levels', 'figure'),
    Output('combo-levels', 'figure')],
    [Input('powell-water-data', 'data'),
    Input('mead-water-data', 'data'),
    Input('combo-water-data', 'data')])
def lake_graphs(powell_data, mead_data, combo_data):
    powell_df = pd.read_json(powell_data)
    mead_df = pd.read_json(mead_data)
    combo_df = pd.read_json(combo_data)

    powell_traces = []
    mead_traces = []
    combo_traces = []

    data = powell_df.sort_index()
    # title = 'Lake Powell'
    powell_traces.append(go.Scatter(
        y = powell_df['Water Level'],
        x = powell_df.index,
        name='Water Level'
    )),

    for column in mead_df.columns[1:]:
        mead_traces.append(go.Scatter(
            y = mead_df[column],
            x = mead_df.index,
            name = column
        ))

    powell_traces.append(go.Scatter(
        y = powell_df['power level'],
        x = powell_df.index,
        name = 'Power level'
    )),

    powell_traces.append(go.Scatter(
        y = powell_df['sick pool'],
        x = powell_df.index,
        name = 'Sick Pool'
    )),

    powell_traces.append(go.Scatter(
        y = powell_df['dead pool'],
        x = powell_df.index,
        name = 'Dead Pool'
    )),

    combo_traces.append(go.Scatter(
        y = combo_df['Water Level'],
        x = combo_df.index,
    ))

    powell_layout = go.Layout(
        height =400,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    mead_layout = go.Layout(
        height = 400,
        title = 'Lake Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    combo_layout = go.Layout(
        height =400,
        title = 'Powell and Mead Total Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )


    time.sleep(2)
    return {'data': powell_traces, 'layout': powell_layout}, {'data': mead_traces, 'layout': mead_layout}, {'data': combo_traces, 'layout': combo_layout}


@app.callback([
    Output('bm-levels', 'figure'),
    Output('navajo-levels', 'figure'),
    Output('fg-levels', 'figure')],
    [Input('blue-mesa-water-data', 'data'),
    Input('navajo-water-data', 'data'),
    Input('fg-water-data', 'data')])
def lake_graph(bm_data, nav_data, fg_data):
    bm_df = pd.read_json(bm_data)
    nav_df = pd.read_json(nav_data)
    fg_df = pd.read_json(fg_data)
    print(fg_df)

    bm_traces = []
    nav_traces = []
    fg_traces = []

    bm_traces.append(go.Scatter(
        y = bm_df['Value'],
        x = bm_df.index,
    ))

    nav_traces.append(go.Scatter(
        y = nav_df['Value'],
        x = nav_df.index,
    ))

    fg_traces.append(go.Scatter(
        y = fg_df['Value'],
        x = fg_df.index,
    ))

    bm_layout = go.Layout(
        height =400,
        title = 'Blue Mesa Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    nav_layout = go.Layout(
        height =400,
        title = 'Navajo Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    fg_layout = go.Layout(
        height =400,
        title = 'Flaming Gorge Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': bm_traces, 'layout': bm_layout}, {'data': nav_traces, 'layout': nav_layout}, {'data': fg_traces, 'layout': fg_layout}

@app.callback([
    Output('drought-graph', 'figure'),
    Output('dsci-graph', 'figure'),
    Output('diff-graph', 'figure'),],
    [Input('combo-water-data', 'data'),
    Input('drought-data', 'data'),
    Input('MA-input', 'value')])
def drought_graphs(combo_data, data, ma_value):
    df = pd.read_json(data)
    # df_last = pd.read_json(last)
    # print(df_last)

    df['MA'] = df['DSCI'].rolling(window=ma_value).mean()
    # print(df)


    drought_traces = []
    dsci_traces = []
    diff_traces = []

    df_combo = pd.read_json(combo_data)
    df_combo['color'] = np.where(df_combo.index.year % 2 == 1, 'lightblue', 'aqua')
    df_combo_last = df_combo.groupby(df_combo.index.strftime('%Y')).tail(1)
    df_combo_last['diff'] = df_combo_last['Water Level'].diff()
    df_combo_last['diff'] = df_combo_last['diff'].apply(lambda x: x*-1)

    print(df_combo_last)
    #adi = annual dsci average

    df_ada = df[['DSCI']]
    df_ada = df_ada.groupby(df_ada.index.strftime('%Y'))['DSCI'].mean()
    # print(df_ada)
    # df_combo_last['diff'] = df_combo_last[]


    drought_traces.append(go.Scatter(
        name='DSCI Mov. Avg.',
        y=df['MA'],
        x=df.index,
        marker_color = 'red',
        yaxis='y'
    )),
    drought_traces.append(go.Bar(
        name='Volume',
        y=df_combo['Water Level'],
        x=df_combo.index,
        yaxis='y2',
        marker_color=df_combo['color']
    )),

    drought_layout = go.Layout(
        height=500,
        title='DSCI and Total Storage',
        yaxis={'title':'DSCI', 'overlaying': 'y2'},
        yaxis2={'title': 'MAF', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    dsci_traces.append(go.Scatter(
        name='Negative Vol.Change',
        y=df_combo_last['diff'],
        x=df_combo_last.index,
        mode='markers',
        marker_size=10,
        yaxis='y',
        marker_color='red',
        # opacity=0.5,
        # width=2
    )),

    dsci_traces.append(go.Bar(
        name='DSCI Annual Mean',
        y=df_ada,
        x=df_combo_last.index,
        yaxis='y2',
        marker_color='blue',
    )),

    

    dsci_layout = go.Layout(
        height= 500,
        title='Mean DSCI and Negative Volume Change',
        yaxis={'title':'MAF', 'overlaying': 'y2'},
        yaxis2={'title': 'DSCI', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    diff_layout = go.Layout(
        height = 500,
        title = 'DSCI',
        yaxis = {'title':'DSCI', 'overlaying': 'y2'},
        yaxis2 = {'title': 'MAF', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': drought_traces, 'layout': drought_layout}, {'data': dsci_traces, 'layout': dsci_layout}, {'data': diff_traces, 'layout': diff_layout}

# @app.callback(
#     Output('drought-graph', 'figure'),
#     [Input('combo-water-data', 'data'),
#     Input('drought-data', 'data')])
# def dsci_diff_graph(combo_data, data):

#################### ANNUAL CHAANGE DATA ###############

@app.callback([
    Output('powell-annual-changes', 'figure'),
    Output('mead-annual-changes', 'figure'),
    Output('combo-annual-changes', 'figure')],
    [Input('powell-annual-change', 'data'),
    Input('mead-annual-change', 'data'),
    Input('combo-annual-change', 'data'),])
def change_graphs(powell_data, mead_data, combo_data):
    df_powell = pd.read_json(powell_data)
    df_mead = pd.read_json(mead_data)
    df_combo = pd.read_json(combo_data)
    pd.set_option('display.max_columns', None)
    # print(df_powell)
    # print(df_mead)
    # df_combo = df_combo.drop(df_combo.columns[[2,3,4,5]], axis=1)
    # print(df_combo)
    # df_powell['diff'] = (df_powell['diff'] !='n').astype(int)

    mead_traces = []
    powell_traces = []
    combo_traces = []

    # data = powell_traces.sort_index()

    powell_traces.append(go.Bar(
        y = df_powell['diff'],
        x = df_powell.index,
        marker_color = df_powell['color']
    )),

    mead_traces.append(go.Bar(
        y = df_mead['diff'],
        x = df_mead.index,
        marker_color = df_mead['color']
    )),

    combo_traces.append(go.Bar(
        y = df_combo['diff'],
        x = df_combo.index,
        marker_color = df_combo['color']
    )),

    powell_layout = go.Layout(
        height =400,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    mead_layout = go.Layout(
        height =400,
        title = 'Lake Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    combo_layout = go.Layout(
        height =400,
        title = 'Powell + Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': powell_traces, 'layout': powell_layout}, {'data': mead_traces, 'layout': mead_layout}, {'data': combo_traces, 'layout': combo_layout}


############################# STATS CALLBACKS #####################################

@app.callback([
    Output('cur-levels', 'children'),
    Output('powell-annual-change', 'data'),
    Output('mead-annual-change', 'data'),
    Output('combo-annual-change', 'data')],
    [Input('powell-water-data', 'data'),
    Input('mead-water-data', 'data'),
    Input('combo-water-data', 'data'),
    Input('interval-component','n_intervals')])
def get_current_volumes(powell_data, mead_data, combo_data, n):
    powell_data = pd.read_json(powell_data)
    powell_data.sort_index()
    powell_current_volume = powell_data.iloc[-1,1]
    powell_current_volume_date = powell_data.index[-1]
    cvd = str(powell_current_volume_date)
    powell_last_v = powell_data.iloc[-1,0]
    powell_pct = powell_current_volume / capacities['Lake Powell Glen Canyon Dam and Powerplant']
    powell_tfh_change = powell_current_volume - powell_data['Water Level'][-2]
    powell_cy = powell_current_volume - powell_data['Water Level'][-days]
    powell_yr = powell_current_volume - powell_data['Water Level'][-366]
    powell_last = powell_data.groupby(powell_data.index.strftime('%Y')).tail(1)
   
    # powell_last['diff'] = powell_last['Value'] - powell_last['Value'].shift(1)
    powell_last['diff'] = powell_last['Water Level'].diff()
    powell_last['color'] = np.where(powell_last['diff'] < 0, 'red', 'green')
   
    powell_annual_min = powell_data.resample('Y').min()
    powell_min_twok = powell_annual_min[(powell_annual_min.index.year > 1999)]
    powell_rec_low = powell_min_twok['Water Level'].min()
    powell_dif_rl = powell_data['Water Level'].iloc[-1] - powell_rec_low
    # powell_rec_diff = powell_current_volume - powel
    
    powell_rec_low_date = powell_data['Water Level'].idxmin().strftime('%Y-%m-%d')
    # print(powell_rec_low_date)

    mead_data = pd.read_json(mead_data)
    mead_data.sort_index()
    mead_current_volume = mead_data.iloc[-0,-0]
    mead_current_volume = mead_data['Water Level'].iloc[-1]
    mead_pct = mead_current_volume / capacities['Lake Mead Hoover Dam and Powerplant']
    mead_last_v = mead_data.iloc[-1,0]
    mead_tfh_change = mead_current_volume - mead_data['Water Level'][-2]
    mead_cy = mead_current_volume - mead_data['Water Level'][-days]
    mead_yr = mead_current_volume - mead_data['Water Level'][-366]
    mead_last = mead_data.groupby(mead_data.index.strftime('%Y')).tail(1)
    mead_annual_min = mead_data.resample('Y').min()
    mead_min_twok = mead_annual_min[(mead_annual_min.index.year > 1999)]
    mead_rec_low = mead_min_twok['Water Level'].min()
    mead_dif_rl = mead_data['Water Level'].iloc[-1] - mead_rec_low
    
    # powell_last['diff'] = powell_last['Value'] - powell_last['Value'].shift(1)
    mead_last['diff'] = mead_last['Water Level'].diff()
    mead_last['color'] = np.where(mead_last['diff'] < 0, 'red', 'green')
    mead_rec_low_date = mead_data['Water Level'].idxmin().strftime('%Y-%m-%d')
   
    combo_data = pd.read_json(combo_data)
    
    combo_current_volume = combo_data['Water Level'][-1]
    combo_current_volume_date = combo_data.index[-1]
    combo_pct = combo_current_volume / capacities['Powell Mead Combo']
    combo_last_v = combo_data['Water Level'][-2]
    combo_tfh_change = combo_current_volume - combo_data['Water Level'][-2]
    combo_cy = combo_current_volume - combo_data['Water Level'][-days]
    combo_yr = combo_current_volume - combo_data['Water Level'][-366]
   
    combo_last = combo_data.groupby(combo_data.index.strftime('%Y')).tail(1)
    combo_last['diff'] = combo_last['Water Level'].diff()
    combo_last['color'] = np.where(combo_last['diff'] < 0, 'red', 'green')
    combo_annual_min = combo_data.resample('Y').min()
    pd.set_option('display.max_columns', None)
    # print(combo_last)
    combo_min_twok = combo_annual_min[(combo_annual_min.index.year > 1999)]
    combo_rec_low = combo_min_twok['Water Level'].min()
    combo_dif_rl = combo_data['Water Level'].iloc[-1] - combo_rec_low
    combo_rec_low_date = combo_data['Water Level'].idxmin().strftime('%Y-%m-%d')


    return html.Div([
        html.Div([
            html.Div([
                html.H6('Powell', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_current_volume), style={'text-align': 'right'})
            ],
                className='two columns'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(powell_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_rec_low), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(powell_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.H6('Mead', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_current_volume), style={'text-align': 'right'})
            ],
                className='two columns'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(mead_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(mead_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.H6('Combined', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_current_volume), style={'text-align': 'right'})
            ],
                className='two columns'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(combo_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_rec_low), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(combo_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
    ]), powell_last.to_json(), mead_last.to_json(), combo_last.to_json(), 

@app.callback(
    Output('upper-cur-levels', 'children'),
    [Input('blue-mesa-water-data', 'data'),
    Input('navajo-water-data', 'data'),
    Input('fg-water-data', 'data'),
    Input('ur-water-data', 'data')])
def get_current_volumes_upper(bm_data, nav_data, fg_data, ur_data):
    bm_data = pd.read_json(bm_data)
    bm_data.sort_index()
    bm_current_volume = bm_data.iloc[-1,1]
    bm_pct = bm_current_volume / capacities['BLUE MESA RESERVOIR']
    bm_tfh_change = bm_current_volume - bm_data['Value'][-2]
    bm_cy = bm_current_volume - bm_data['Value'][-days]
    bm_yr = bm_current_volume - bm_data['Value'][-366]
    bm_rec_low = bm_data['Value'].min()
    bm_dif_rl = bm_data['Value'].iloc[-1] - bm_rec_low
    bm_rec_low_date = bm_data['Value'].idxmin().strftime('%Y-%m-%d')


    nav_data = pd.read_json(nav_data)
    nav_data.sort_index()
    nav_current_volume = nav_data.iloc[-1,1]
    nav_pct = nav_current_volume / capacities['NAVAJO RESERVOIR']
    nav_tfh_change = nav_current_volume - nav_data['Value'][-2]
    nav_cy = nav_current_volume - nav_data['Value'][-days]
    nav_yr = nav_current_volume - nav_data['Value'][-366]
    nav_rec_low = nav_data['Value'].min()
    nav_dif_rl = nav_data['Value'].iloc[-1] - nav_rec_low
    nav_rec_low_date = nav_data['Value'].idxmin().strftime('%Y-%m-%d')

    fg_data = pd.read_json(fg_data)
    fg_data.sort_index()
    fg_current_volume = fg_data.iloc[-1,1]
    fg_pct = fg_current_volume / capacities['FLAMING GORGE RESERVOIR']
    fg_tfh_change = fg_current_volume - fg_data['Value'][-2]
    fg_cy = fg_current_volume - fg_data['Value'][-days]
    fg_yr = fg_current_volume - fg_data['Value'][-366]
    fg_rec_low = fg_data['Value'].min()
    fg_dif_rl = fg_data['Value'].iloc[-1] - fg_rec_low
    fg_rec_low_date = fg_data['Value'].idxmin().strftime('%Y-%m-%d')

    ur_data = pd.read_json(ur_data)
    print(ur_data)
    ur_data['Storage'] = ur_data['Value_x'] + ur_data['Value_y'] + ur_data['Value']
    print(ur_data)
    ur_current_volume = ur_data['Storage'].iloc[-1]
    ur_pct = ur_current_volume / capacities['UR']
    ur_tfh_change = ur_current_volume - ur_data['Storage'][-2]
    ur_cy = ur_current_volume - ur_data['Storage'][-days]
    ur_yr = ur_current_volume - ur_data['Storage'][-366]
    ur_rec_low = ur_data['Storage'].min()
    ur_dif_rl = ur_data['Storage'].iloc[-1] - ur_rec_low
    ur_rec_low_date = ur_data['Storage'].idxmin().strftime('%Y-%m-%d')
 

    return html.Div([
        html.Div([
            html.Div([
                html.H6('Blue Mesa', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(bm_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(bm_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([
                html.H6('Navajo', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(nav_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(nav_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([
                html.H6('Flaming Gorge', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(fg_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(fg_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([
                html.H6('Combined', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(ur_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(ur_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
    ])

if __name__ == '__main__':
    app.run_server(port=8000, debug=True)
