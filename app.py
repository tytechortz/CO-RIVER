import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import flask


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

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
                href='/apps/ur'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Drought'),
                href='/apps/drought'
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

def home_page_App():
    return html.Div([
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
        # dcc.Store(id='powell-water-data'),
        # dcc.Store(id='mead-water-data'),
        # dcc.Store(id='combo-water-data'),
        # dcc.Store(id='powell-annual-change'),
        # dcc.Store(id='mead-annual-change'),
        # dcc.Store(id='combo-annual-change'),
    ])

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

homepage = html.Div([
    home_page_App(),
    # dcc.Link('Upper Reservoirs"', href='/page-1'),
    # html.Br(),
    # dcc.Link('Navigate to "/page-2"', href='/page-2'),
])

layout_page_1 = html.Div([
    get_header(),
    # dcc.Input(id='input-1-state', type='text', value='Montreal'),
    # dcc.Input(id='input-2-state', type='text', value='Canada'),
    # html.Button(id='submit-button', n_clicks=0, children='Submit'),
    # html.Div(id='output-state'),
    # html.Br(),
    # dcc.Link('Navigate to "/"', href='/'),
    # html.Br(),
    # dcc.Link('Navigate to "/page-2"', href='/page-2'),
])

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    homepage,
    layout_page_1,
    # layout_page_2,
])

# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return homepage
    elif pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
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

if __name__ == '__main__':
    app.run_server(debug=True)
