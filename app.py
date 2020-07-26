import requests
import json
import argparse
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
from scipy.ndimage import gaussian_gradient_magnitude
import multidict
from PIL import Image
from io import BytesIO
import base64
import iconfonts
import dash_dangerously_set_inner_html
from datetime import datetime, date, timedelta
from dateutil.relativedelta import *
# import flask


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
we = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
we1 = 'https://use.fontawesome.com/releases/v5.8.2/css/all.css'
we2 = 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap'
we3 = 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css'
we4 = 'https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.0/css/mdb.min.css'
we5 = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
# wet = "https://github.com/lipis/bootstrap-social/blob/gh-pages/bootstrap-social.css"
external_stylesheets = dbc.themes.DARKLY
# server = flask.Flask(__name__)

sc1 = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js'
sc2 = 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.4/umd/popper.min.js'
sc3 = 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.min.js'
sc4 = 'https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.0/js/mdb.min.js'
sc5 = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js'

colors = {
    'background': '#222',
    'text': '#fff',
    'warn': '#CF6679',
    'dimInput': '#696969'
}
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets], external_scripts=["https://buttons.github.io/buttons.js"])
app.title = 'KYCS - Know Your CodeForces Submissions'
server = app.server

verdicts = set()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

app.layout = html.Div(id='main', children=[ 
    html.Header([
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
            <script async defer src="https://buttons.github.io/buttons.js"></script>
        ''')
    ]),
    html.Div(id='hell', children=[
    dbc.Navbar(
        [
            # html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(className="", style={'color':'white'},children=[
                            html.H4("Welcome To [ KYCS ]"),
                            html.H5("Know Your CodeForces Submissions")
                        ])),
                    ],
                ),
                dbc.Row(
                    [
                        html.Div(children=[
                            # dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                            #     <!-- Place this tag where you want the button to render. -->
                            #     <iframe src="https://ghbtns.com/github-btn.html?user=JeetKaria06&repo=KYCS&type=star&count=false&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>
                            # '''),
                            dbc.Button(html.Span(["Learn More", html.Img(src="https://image.flaticon.com/icons/svg/702/702797.svg")]), color="primary", id="open-xl")
                        ], style={'margin-right':'15px'})
                    ],
                    className="ml-auto"
                )
                # html.Br(),
                # dbc.Row(
                #     [
                #         # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                #         dbc.Col(dbc.NavbarBrand(html.H5("Know Your CodeForces Submissions"), className="ml-2")),
                #     ],
                #     align="center",
                #     # no_gutters=True,
                # ),
                # href="https://plot.ly",
            # )
            # dbc.NavbarToggler(id="navbar-toggler"),
            # dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
        ],
        color="dark",
        dark=True
    ),
    html.Br(),
    html.Br(),
    # html.Div(id='header1', children=[]),
    html.Center(
        html.Div(children=[
        html.P('Enter Your Handle Below'),
        dbc.Input(id='my-id', placeholder='Enter Your Handle Here', type='text', style={'backgroundColor':colors['text'], 'max-width':'18rem'}),
        html.Br()
        ])
    ),

    html.Center(html.Button('Submit', type="button", className="btn btn-outline-info", id='submit-val', n_clicks=0)),
    # html.Div(id='fig'),
    dcc.Loading(id = "load", 
        children=[html.Center(html.Div(className='badge badge-danger',id="my-div", children=''))], type="default", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H3(
        children='Submission Distribution Verdictwise',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
    dcc.Loading(id = "loading0", 
        children=[html.Div(dcc.Graph(id='fig0'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Submission Distribution Verdict+Ratingwise',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
     dcc.Loading(id = "loading", 
            children=[html.Div(dcc.Graph(id='fig'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
        html.H3(
        children='Submission Distribution Tags+Verdictwise',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
     dcc.Loading(id = "loading-1", 
            children=[html.Div(dcc.Graph(id='fig-1'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Submission Distribution Tags+Verdict+Ratingwise',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
     dcc.Loading(id = "loading1", 
            children=[html.Div(dcc.Graph(id='fig1'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Submissions with Month on the x-axis',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
    dcc.Loading(id = "loading_Avg", 
            children=[], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children="Submissions Bifurcated based on Problem's Indices",
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
    dcc.Loading(id = "loading_index", 
            children=[], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='WordClound of the tags based on your Submissions',
        style={
            'textAlign': 'center',
            'color': '#BB86FC'
        },
        # className="text-info"
    ),
    html.Br(),
    dcc.Loading(id = "loadingimg", 
            children=[html.Center(html.Img(id="image_wc", style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    # html.Center(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''<div id='shareButton' class="fb-share-button" data-href="https://kycs.herokuapp.com/" data-layout="button_count" data-size="small"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https://kycs.herokuapp.com/;src=sdkpreparse" class="fb-xfbml-parse-ignore">Share</a></div>''')),
    html.Br(),
    html.Br(),
    html.Center(
        html.Div(
            className='jumbotron',
            children=[
                
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                        <a class="btn-social btn-facebook" href="https://www.facebook.com/profile.php?id=100006146385849">
                            <span class="fa fa-facebook"></span>
                        </a>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <a class="btn-social btn-github" href="https://github.com/JeetKaria06">
                            <span class="fa fa-github"></span>
                        </a>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <a class="btn-social btn-instagram" href="https://instagram.com/karia_jeet">
                            <span class="fa fa-instagram"></span>
                        </a>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <a class="btn-social btn-linkedin" href="https://www.linkedin.com/in/jeet-karia-628773170/">
                            <span class="fa fa-linkedin"></span>
                        </a>
                '''),
                html.Br(),
                html.Br(),
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                    <center><iframe src="https://ghbtns.com/github-btn.html?user=JeetKaria06&repo=KYCS&type=star&count=true&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>
                    </center>
                '''),
                html.Br(),
                html.Br(),
                dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''<h5> Developed by [ <a href="https://codeforces.com/profile/Jeet_Karia">Jeet_Karia</a> ]</h5>'''),
            #    html.Center(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
            #         <iframe src="https://ghbtns.com/github-btn.html?user=JeetKaria06&repo=KYCS&type=star&count=false&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>
            #     '''))
            ]
        )
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("[ KYCS ] Python App"),
            dbc.ModalBody([
                html.H3("What is this app about?"),
                html.H5("This app lets you analyze your codeforces submissions and visualizing them in comman man's manner."),
                html.H3("What makes it different than other apps/tools ?"),
                html.H5("(i) Allows you to keep track of your average monthly submissions and even separating it on particular month."),
                html.H5("(ii) Wordcloud makes one realize his/her go to domain for problem solving."),
                html.H5("(iii) Interactive plots makes it different in the league."),
                html.H5("(iv) Last but not the least is THE DARK USER-FRIENDLY THEME.")
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-xl", className="ml-auto", color="primary")
            ),
        ],
        id="modal-xl",
        size="xl",
    ),
    dcc.Loading(id = "loading_use", 
            children=[
                html.Div(
                [
                    dbc.Button(
                        "Stuck? Press Me  : )", id="popover-target", style={'backgroundColor':'#FF7597', 'color':'#000'}
                    ),
                    dbc.Popover(
                        [],
                        id="popover",
                        is_open=False,
                        target="popover-target",
                    ),
                ],
                style={'position':'fixed', 'top':200}
            )],
            type="circle", 
            fullscreen=False,
            debug=False,
            style={'align':'center'}
    ),
])
])


@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [dash.dependencies.State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [dash.dependencies.State("modal-xl", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='loading_index', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_index(n_clicks, input_value):  # Index bar chart
    handle = input_value
    if handle==None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig_index'))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig_index'))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig_index'))
        # exit()

    stat = response.json()['result']
    color = ['#0dba2f', '#F4511E', '#4A148C',
          'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
          'rgba(190, 192, 213, 1)']
    
    data = {}
    totalData = {}
    for submission in stat:
        index = submission['problem']['index'][0]
        pname = submission['problem']['name']
        verdict = submission['verdict']

        if verdict not in data.keys():
            data[verdict] = {}

        if index not in data[verdict].keys():
            data[verdict][index] = set()
        
        data[verdict][index].add(pname)

        if index not in totalData.keys():
            totalData[index] = {}
        if verdict not in totalData[index].keys():
            totalData[index][verdict] = set()
        
        totalData[index][verdict].add(pname)
    mx=0
    for kes in totalData.keys():
        cnt=0
        for verdict in totalData[kes].keys():
            totalData[kes][verdict] = len(totalData[kes][verdict])
            cnt += totalData[kes][verdict]
        totalData[kes] = cnt
        mx = max(mx, cnt) 

    fig = go.Figure()
    i=0
    for verds in data.keys():
        arr = []
        rate = []
        for indices in sorted(data[verds].keys()):
            data[verds][indices] = len(data[verds][indices])
            arr.append(data[verds][indices])
            rate.append(str(round(data[verds][indices]/totalData[indices]*100, 2)))

        fig.add_trace(go.Bar(
            x = list(sorted(data[verds].keys())),
            y = arr,
            width=0.6,
            # height=20,
            name = verds,
            orientation = 'v',
            marker = dict(
                color = color[i%6],
                line = dict(color='#222', width=0.5)
            ),
            showlegend = True,
            # font=dict(color="white"),
            text = rate,
            hovertemplate = "Rate of <i>"+verds+"</i><br> %{text}<b> %</b> <br> Unique <i>"+verds+"</i> Submissions: %{y}",
            # textposition='auto',
            hoverlabel = dict(font=dict(size=23))
        ))
        i+=1        

    fig.update_layout(
            barmode='stack',
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=25,
                    color='white',
                )
            ),
            yaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=25,
                    color='white',
                ),
            ),
            height=800,
            plot_bgcolor='#222',
            paper_bgcolor='#222',
            legend=dict(font=dict(color='white'))
        )

    for index in totalData.keys():
        fig.add_annotation(
            text=str(totalData[index]),
            x=index,
            y=totalData[index]+30*mx/800,
            # font=dict(color='white', size=20),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=20,
                color="white"
            ),
            align="center",       
            bordercolor="#3700B3",
            borderwidth=2,
            borderpad=2,
            bgcolor="#121212",
            opacity=1
        )
    
    return html.Div(dcc.Graph(figure=fig, id='fig_index'))

@app.callback(
    Output('loading_Avg', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('my-id', 'value')]
)
def show_avg(n_clicks, input_value): # Show Average
    handle = input_value
    if handle == None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig))

    try:
        response = requests.get("https://codeforces.com/api/user.info?handles="+handle)
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig))

    state = response.json()['result']
    global regDate
    regDate = datetime.utcfromtimestamp(int(state[0]['registrationTimeSeconds']))
    regDate = date(regDate.year, regDate.month, regDate.day)

    try:
        responsen = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    stat = responsen.json()['result']

    verdicts.clear()
    global mdict
    mdict = {}

    for submission in stat:
        submissionsDate = datetime.utcfromtimestamp(int(submission['creationTimeSeconds']))
        submissionsDate = date(submissionsDate.year, submissionsDate.month, submissionsDate.day)
        pname = submission['problem']['name']
        verdict = submission['verdict']
        verdicts.add(verdict)
        
        if str(submissionsDate.month)+'-'+str(submissionsDate.year) not in mdict.keys():
            mdict[str(submissionsDate.month)+'-'+str(submissionsDate.year)]={}
        
        if verdict not in mdict[str(submissionsDate.month)+'-'+str(submissionsDate.year)].keys():
            mdict[str(submissionsDate.month)+'-'+str(submissionsDate.year)][verdict]=[]

        mdict[str(submissionsDate.month)+'-'+str(submissionsDate.year)][verdict].append(pname)

    cnt=0
    for dat in mdict.keys():
        for verdict in mdict[dat].keys():
            mdict[dat][verdict] = len(set(mdict[dat][verdict]))
    # print(mdict)
    # return 
    # html.Center(
        # html.Div(children=[
    return [
            html.Br(),
            html.Center(html.H4("Select starting Month and Year", className="text-success")),
            html.Center(dbc.Select(
                    id='start_month',
                    options=[{'label': months[i], 'value': i } for i in range(12)],
                    # searchable=True,
                    className="mb-3",
                    style={'width':'35%'}
                )
            ),
            # html.Br(),
            html.Center(dbc.Select(
                id='start_year',
                options=[{'label': i, 'value': i } for i in range(regDate.year, date.today().year+1)],
                # searchable=True,
                className="mb-3",
                style={'width':'35%'}
            )),
            html.Center(html.H4("Select ending Month and Year", className="text-success")),
            html.Center(dbc.Select(
                id='end_month',
                options=[{'label': months[i], 'value': i } for i in range(12)],
                # searchable=True
                className="mb-3",
                style={'width':'35%'}
            )),
            # html.Br(),
            html.Center(dbc.Select(
                id='end_year',
                options=[{'label': i, 'value': i } for i in range(regDate.year, date.today().year+1)],
                # searchable=True,
                className="mb-3",
                style={'width':'35%'}
            )),
            html.Br(),
            html.Center(html.H4("Choose a feature", className="text-success")),
            html.Center(dbc.Select(
                id='caf',
                options=[{'label': 'Average Submissions', 'value': 0}, {'label': 'Cumulative Submissions', 'value': 1}, {'label': 'Individual Submissions', 'value': 2}],
                className="mb-3",
                style={'width':'35%'}
            )),
            html.Br(),
            html.Center(html.H4("Checked Options Will be Counted in the Average Calculation.", className="text-success")),
            html.Center(dcc.Checklist(
                id='checklist',
                inputStyle={"margin-right": "7px", "margin-left":"22px"},
                options=[{'label':ve, 'value':ve} for ve in verdicts],
                value=list(verdicts),
                labelStyle={'display': 'inline-block'},
                className="custom-control custom-checkbox"
                # labelClassName="custom-control-label"
            )),
            html.Br(),
            html.Br(),  
            html.Center(dcc.Loading(id = "loading_avg", 
                children=[], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0})
            )    
    ]
    # ))

@app.callback(
    Output(component_id='loading_avg', component_property='children'),
    [Input('start_year', 'value'),
     Input('start_month', 'value'), 
     Input('end_year', 'value'), 
     Input('end_month', 'value'),
     Input('caf', 'value'),
     Input('checklist', 'value')]
)
def update_output(start_year, start_month, end_year, end_month, caf, value): #Avg Line chart
    if(start_year==None or start_month==None or end_year==None or caf==None or end_month==None or (end_year < start_year or (end_year==start_year and end_month<start_month))):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Please Pick the Valid Range.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig_avg'))
    
    start_month = int(start_month)
    end_month = int(end_month)
    
    start_year = int(start_year)
    end_year = int(end_year)

    start_month += 1
    end_month += 1
    # print('ola')
    # print(mdict)
    start = str(start_month)+'-'+str(start_year)
    end = str(end_month)+'-'+str(end_year)

    sdate = max(date(regDate.year, regDate.month, 1), date(start_year, start_month, 1))
    edate = date(end_year, end_month, 1)
    
    dfplot = pd.DataFrame({'Month': [], 'Subs': []})
    hola = ['Avg Subs', 'Cumulative Subs', 'Individual Subs']
    cnt=0
    subs=0
    
    while sdate<=min(edate, date(date.today().year, date.today().month, 1)):
        sep=0
        artkey = str(sdate.month)+'-'+str(sdate.year)
        cnt+=1

        if artkey not in mdict.keys():
            mdict[artkey] = {}
            for vs in verdicts:
                mdict[artkey][vs] = 0
        else:
            for vs in verdicts:
                if vs not in mdict[artkey].keys():
                    mdict[artkey][vs]=0
        
        for vs in verdicts:
            if vs in value:
                sep += mdict[artkey][vs]
                subs += mdict[artkey][vs]

        if caf=='0':
            dfplot = dfplot.append({'Month':months[sdate.month-1]+" "+str(sdate.year), 'Subs':subs/cnt}, ignore_index=True)
        elif caf=='1':
            dfplot = dfplot.append({'Month':months[sdate.month-1]+" "+str(sdate.year), 'Subs':subs}, ignore_index=True)
        else:
            dfplot = dfplot.append({'Month':months[sdate.month-1]+" "+str(sdate.year), 'Subs':sep}, ignore_index=True)

        sdate += relativedelta(months=1)
    # fig_final = make_subplots(rows=3, cols=1)
    # fig = go.Figure()

    fig = go.Figure(go.Scatter(
        x=list(dfplot['Month']),
        y=list(dfplot['Subs']),
        # name='Average Accepted Submissions',
        # line=dict(color='royalblue', width=4, dash='dot')
        # font=dict(color='royalblue'),
        mode='lines+markers',
        hovertemplate="<i>When?</i>   <b>%{x}</b>"+"<br><b><i>"+hola[int(caf)]+":</i></b> %{y:.2f}"
    ))
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=15,
                color='white',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=15,
                color='white',
            ),
        ),
        plot_bgcolor='#222',
        paper_bgcolor='#222'
    )

    return html.Div(dcc.Graph(figure=fig, id='fig_avg'))    

@app.callback(
    Output('popover', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('my-id', 'value')]
)
def update_header(n_clicks, input_value):
    handle = input_value
    returndivs = []
    if input_value==None:
        return html.Div(id='header', className='card text-white bg-primary mb-3', style={}, 
                        children=[html.Div(
                                'Blue Card',
                                className='card-header',
                                style={
                                    #'backgroundColor':colors['background'], 
                                    'color':colors['text']
                                },
                            ),
                            html.Div(
                                className='card-body',
                                style={
                                    'color':colors['text']
                                },
                                children=[
                                    html.H4('Enter the handle', className='card-title'),
                                    html.P("Enter the user handle of codeforces in the box appearing right to you and left to me. Now go on don't shy out.",className='card-text')
                                ]
                            )
                            ]
                        )

    try:
        response = requests.get("https://codeforces.com/api/user.info?handles="+handle)
    except requests.exceptions.RequestException as e:
        # html.Div(id='')
        return html.Div(id='header', className='card text-white bg-danger mb-3', style={}, 
                        children=[html.Div(
                                'Red Card',
                                className='card-header',
                                style={
                                    #'backgroundColor':colors['background'], 
                                    'color':colors['text']
                                },
                            ),
                            html.Div(
                                className='card-body',
                                style={
                                    'color':colors['text']
                                },
                                children=[
                                    html.H4("Site isn't reached.", className='card-title'),
                                    html.P("There are 2 reasons for this to happen: 1-Either Your Internet Connection is Broken 2-Site is taking too long to respond back.",className='card-text')
                                ]
                            )
                            ]
                        )

    if response.status_code==400:
        return html.Div(id='header', className='card text-white bg-warning mb-3', style={}, 
                        children=[html.Div(
                                'Yellow Card',
                                className='card-header',
                                style={
                                    #'backgroundColor':colors['background'], 
                                    'color':colors['text']
                                },
                            ),
                            html.Div(
                                className='card-body',
                                style={
                                    'color':colors['text']
                                },
                                children=[
                                    html.H4('Invalid Handle', className='card-title'),
                                    html.P("The handle that you have entered doesn't seem to exist in the CodeForces. Check the spelling.",className='card-text')
                                ]
                            )
                            ]
                        )
    else:
        return html.Div(id='header', className='card text-white bg-success mb-3', style={}, 
                        children=[html.Div(
                                'Green Card',
                                className='card-header',
                                style={
                                    #'backgroundColor':colors['background'], 
                                    'color':colors['text']
                                },
                            ),
                            html.Img(
                                className="card-img-top",
                                src=response.json()['result'][0]['titlePhoto'],
                                alt="Image doesn't exists",
                                style = {}
                            ),
                            html.Div(
                                className='card-body',
                                style={
                                    'color':colors['text']
                                },
                                children=[
                                    html.H4('Enjoy the stay', className='card-title'),
                                    html.P("The handle is being loaded. If it misses out anything from below, then press submit again because sometimes dash misbehaves.",className='card-text')
                                ]
                            ),
                            html.Div(
                                className="card-footer",
                                children=[
                                    html.Small(
                                        'Rank: ' + response.json()['result'][0]['rank'],
                                        className="text-muted"
                                    )
                                ]
                            )
                            ]
                        )

@app.callback(
    Output('loadingimg', 'children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_wc(n_clicks, input_value):
    handle=input_value
    if handle==None:
        return html.Center(html.Img(id="image_wc", src='', style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))
    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return html.Center(html.Img(id="image_wc", src='', style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))

    if(response.status_code==400):
        return html.Center(html.Img(id="image_wc", src='', style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))
        # exit()

    stat = response.json()['result']

    dfSub = pd.DataFrame({'tag': [], 'frequency': []})
    fullTermsDict = multidict.MultiDict()

    for submission in stat:
        # print(submission)
        # print()
        for tag in submission['problem']['tags']:
            if tag in np.array(dfSub.tag):
                dfSub.loc[dfSub['tag']==tag, 'frequency']=int(dfSub.loc[dfSub['tag']==tag, 'frequency']+1)
            else:
                dfSub = dfSub.append({'tag': tag, 'frequency': int(1)}, ignore_index=True)

    for i, j in dfSub.iterrows():
        #print(j.tag, j.frequency)
        fullTermsDict.add(j.tag, j.frequency)
    

    python_color = np.array(Image.open("lightPython.png"))
    # subsample by factor of 3. Very lossy but for a wordcloud we don't really care.
    python_color = python_color[::3, ::3]

    python_mask = python_color.copy()

    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
    edges = np.mean([gaussian_gradient_magnitude(python_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
    python_mask[edges > .08] = 255

    # create wordcloud. A bit sluggish, you can subsample more strongly for quicker rendering
    # relative_scaling=0 means the frequencies in the data are reflected less
    # acurately but it makes a better picture
    wc = WordCloud(max_words=5000, mask=python_mask, max_font_size=40, random_state=30, relative_scaling=0)

    # generate word cloud
    wc.generate_from_frequencies(fullTermsDict)
    # plt.imshow(wc)

    # create coloring from image
    image_colors = ImageColorGenerator(python_color)
    wc.recolor(color_func=image_colors)
    wc_img = wc.to_image()
    

    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()

    return html.Center(html.Img(id="image_wc", src='data:image/png;base64,'+img2, alt="Enter Valid User Handle", style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='loading0', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]
)
def update_output_die(n_clicks, input_value):  # Only Verdict wise
    handle = input_value
    if handle==None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig0'))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig0'))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig0'))
        # exit()

    stat = response.json()['result']
        
    tot = []
    subData = {}
    subNum = {}
    for submission in stat:
        tot.append(submission['verdict'])
        subData[submission['verdict']] = []

    for submission in stat:
        s = {submission['verdict']: submission['problem']['name']}
        subData[submission['verdict']].append(submission['problem']['name'])

    dfSub = pd.DataFrame({'verdict': [], 'Number': []})

    for verdict in set(tot):
        subNum[verdict] = len(set(subData[verdict]))
        dfSub = dfSub.append({'verdict': verdict, 'Number': subNum[verdict]}, ignore_index=True)

    fig = px.pie(dfSub, values='Number', names='verdict', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide', plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'], font=dict(color=colors['text']))
    return html.Div(dcc.Graph(figure=fig, id='fig0'))

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='loading-1', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_output_div(n_clicks, input_value):       # tag and verdict combined
    handle = input_value
    if handle==None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig-1'))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig-1'))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        }
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig-1'))
        # exit()

    stat = response.json()['result']

    subDict = {}

    for submission in stat:
        # print(submission)
        # print()
        for tag in submission['problem']['tags']:
            if tag not in subDict.keys():
                subDict[tag] = {}
            if submission['verdict'] not in subDict[tag].keys():
                subDict[tag][submission['verdict']] = {}
            if 'rating' in submission['problem'].keys():
                subDict[tag][submission['verdict']][str(submission['problem']['rating'])] = []
            else:
                subDict[tag][submission['verdict']]['unrated'] = []

    # print(subDict)

    for submission in stat:
        for tag in submission['problem']['tags']:
            if 'rating' in submission['problem'].keys():
                subDict[tag][submission['verdict']][str(submission['problem']['rating'])].append(submission['problem']['name'])
            else:
                subDict[tag][submission['verdict']]['unrated'].append(submission['problem']['name'])

    subData = {}
    dfSub = pd.DataFrame({'tag': [], 'verdict': [], 'rating': [], 'number': []})

    for tag in subDict:
        subData[tag] = subDict[tag]
        for verdict in subDict[tag]:
            for rating in subDict[tag][verdict]:
                subData[tag][verdict][rating] = len(set(subDict[tag][verdict][rating]))
                if rating == 'unrated':
                    dfSub = dfSub.append({'tag': tag, 'verdict': verdict, 'rating': 'UNRATED', 'number': subData[tag][verdict][rating]}, ignore_index=True)
                else:
                    dfSub = dfSub.append({'tag': tag, 'verdict': verdict, 'rating': rating, 'number': subData[tag][verdict][rating]}, ignore_index=True)

    # print(dfSub)

    fig = px.sunburst(dfSub, values='number', path=['tag', 'verdict'])
    # fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide')
    fig.update_layout(margin = dict(l=0, r=0, b=0), plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'], font=dict(color=colors['text']))
    return html.Div(dcc.Graph(figure=fig, id='fig-1'))

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='loading1', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_output_diven(n_clicks, input_value):       # tag, verdict and rating combined
    handle = input_value

    if handle==None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig1'))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig1'))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        }
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig1'))
        # exit()

    stat = response.json()['result']

    subDict = {}

    for submission in stat:
        # print(submission)
        # print()
        for tag in submission['problem']['tags']:
            if tag not in subDict.keys():
                subDict[tag] = {}
            if submission['verdict'] not in subDict[tag].keys():
                subDict[tag][submission['verdict']] = {}
            if 'rating' in submission['problem'].keys():
                subDict[tag][submission['verdict']][str(submission['problem']['rating'])] = []
            else:
                subDict[tag][submission['verdict']]['unrated'] = []

    # print(subDict)

    for submission in stat:
        for tag in submission['problem']['tags']:
            if 'rating' in submission['problem'].keys():
                subDict[tag][submission['verdict']][str(submission['problem']['rating'])].append(submission['problem']['name'])
            else:
                subDict[tag][submission['verdict']]['unrated'].append(submission['problem']['name'])

    subData = {}
    dfSub = pd.DataFrame({'tag': [], 'verdict': [], 'rating': [], 'number': []})

    for tag in subDict:
        subData[tag] = subDict[tag]
        for verdict in subDict[tag]:
            for rating in subDict[tag][verdict]:
                subData[tag][verdict][rating] = len(set(subDict[tag][verdict][rating]))
                if rating == 'unrated':
                    dfSub = dfSub.append({'tag': tag, 'verdict': verdict, 'rating': 'UNRATED', 'number': subData[tag][verdict][rating]}, ignore_index=True)
                else:
                    dfSub = dfSub.append({'tag': tag, 'verdict': verdict, 'rating': rating, 'number': subData[tag][verdict][rating]}, ignore_index=True)

    # print(dfSub)

    fig = px.sunburst(dfSub, values='number', path=['tag', 'verdict', 'rating'])
    # fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide')
    fig.update_layout(margin = dict(l=0, r=0, b=0), plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'], font=dict(color=colors['text']))
    return html.Div(dcc.Graph(figure=fig, id='fig1'))

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='loading', component_property='children'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_output_dive(n_clicks, input_value):             # Verdict and Rating combined
    handle = input_value

    if handle==None:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching Data found.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig'))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Codeforces can't be reached at a moment X( Try Again Later.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        },
                        "bgcolor": colors['background']
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig'))

    if(response.status_code==400):
        fig= {
            "layout": {
                "plot_bgcolor": colors['background'],
                "paper_bgcolor":colors['background'],
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No such handle exists :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28,
                            "color": colors['warn']
                        }
                    }
                ]
            }
        }
        return html.Div(dcc.Graph(figure=fig, id='fig'))
        # exit()

    stat = response.json()['result']
        
    tot = []
    subData = {}
    subDataRate = {}
    subNum = {}
    for submission in stat:
        # print(submission)
        tot.append(submission['verdict'])
        if((submission['verdict'] in subData.keys())==False):
            subData[submission['verdict']] = {}
            subData[submission['verdict']]['rating'] = {}
            subData[submission['verdict']]['tag'] = {}
        # print(submission)
        if('rating' in submission['problem'].keys()):
            subData[submission['verdict']]['rating'][str(submission['problem']['rating'])] = []
        else:
            subData[submission['verdict']]['rating']['unrated'] = []
        for tag in submission['problem']['tags']:
            subData[submission['verdict']]['tag'][tag] = []

    for submission in stat:
        if('rating' in submission['problem'].keys()):
            subData[submission['verdict']]['rating'][str(submission['problem']['rating'])].append(submission['problem']['name'])
        else:
            subData[submission['verdict']]['rating']['unrated'].append(submission['problem']['name'])
        for tag in submission['problem']['tags']: 
            subData[submission['verdict']]['tag'][tag].append(submission['problem']['name'])

    dfSubRate = pd.DataFrame({'verdict': [], 'rating': [], 'Number': []})
    # print(subData)
    for verdict in set(tot):
        subNum[verdict] = subData[verdict]
        for rating in subData[verdict]['rating']:
            subNum[verdict]['rating'][rating] = len(set(subData[verdict]['rating'][rating]))
            if rating=='unrated':
                dfSubRate = dfSubRate.append({'verdict': verdict, 'rating': "UNRATED", 'Number': subNum[verdict]['rating'][rating]}, ignore_index=True)
            else:
                dfSubRate = dfSubRate.append({'verdict': verdict, 'rating': rating, 'Number': subNum[verdict]['rating'][rating]}, ignore_index=True)

    # print(dfSubRate.verdict)
    
    fig = px.sunburst(dfSubRate, values='Number', path=['verdict', 'rating'], color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(margin = dict(l=0, r=0, b=0), plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'], font=dict(color=colors['text']))
    return html.Div(dcc.Graph(figure=fig, id='fig'))
@app.callback(
    Output(component_id='load', component_property='children'),
    # Output(component_id='fig1', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_output(n_clicks, input_value):               # Valid User
    handle = input_value
    
    if handle==None:
        return html.Center(html.Div(className='badge badge-danger',id="my-div", children="Enter the Handle :|"))

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return html.Center(html.Div(className='badge badge-danger',id="my-div", children="Host Didn't responded!"))    

    if(response.status_code==400):
        return html.Center(html.Div(className='badge badge-danger',id="my-div", children="No such user exists :( "))
        # exit()
    else:
        return html.Center(html.Div(className='badge badge-danger',id="my-div", children="Handle is being loaded."))

if __name__ == '__main__':
    app.run_server(debug=True)
