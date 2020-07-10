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
# import flask


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
we = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
external_stylesheets = dbc.themes.DARKLY
# server = flask.Flask(__name__)

colors = {
    'background': '#222',
    'text': '#fff',
    'warn': '#FFFF00',
    'dimInput': '#696969'
}
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets, we])
server = app.server

verdicts = set()
finalData = {}
app.layout = html.Div(id='main', children=[ 
    html.Div(id='hell', children=[
    html.H1(
        children='Welcome To [ KYCS ]',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(id='header1', 
    children=[]
    ),
    html.H5(children='{ Know Your Codeforces Submission. }', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Br(),
    html.Br(),
    
    html.Center(
        html.Div( children=[
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
    html.H3(
        children='Submission Distribution Verdictwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Loading(id = "loading0", 
        children=[html.Div(dcc.Graph(id='fig0'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Submission Distribution Verdict+Ratingwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
     dcc.Loading(id = "loading", 
            children=[html.Div(dcc.Graph(id='fig'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
        html.H3(
        children='Submission Distribution Tags+Verdictwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
     dcc.Loading(id = "loading-1", 
            children=[html.Div(dcc.Graph(id='fig-1'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Submission Distribution Tags+Verdict+Ratingwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
     dcc.Loading(id = "loading1", 
            children=[html.Div(dcc.Graph(id='fig1'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='Average number of submissions with date on the x-axis',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Loading(id = "loading_Avg", 
            children=[], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0}),
    html.Br(),
    html.H3(
        children='WordClound of the tags based on your Submissions',
        style={
            'textAlign': 'center'
        },
        className="text-info"
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
                html.H1('developed by [ Jeet_Karia ]'),
                html.Br(),
                dbc.Button(' GitHub', className='fa fa-github', size='lg',href='https://github.com/JeetKaria06', style={'backgroundColor':'#000000', 'width':'10%'}),
                html.Br(),
                dbc.Button(' LinkedIN', className='fa fa-linkedin', size='lg',href='https://www.linkedin.com/in/jeet-karia-628773170/', style={'backgroundColor':'#2867B2', 'width':'10%'}),
                html.Br(),
                dbc.Button(' Instagram', className='fa fa-instagram', size='lg',href='https://instagram.com/karia_jeet', style={'backgroundColor':'#C13584', 'width':'10%'}),
                html.Br(),
                dbc.Button(' Facebook', className='fa fa-facebook', size='lg', href='https://www.facebook.com/profile.php?id=100006146385849', style={'backgroundColor':'#4267B2', 'width':'10%'})
            ]
        )
    )
])
])

@app.callback(
    Output('loading_Avg', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('my-id', 'value')]
)
def show_avg(n_clicks, input_value): # Show Average
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
        return html.Div(dcc.Graph(figure=fig))

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

    stat = response.json()['result']

    verdicts.clear()
    mdict = {}

    for submission in stat:
        submissionsDate = datetime.utcfromtimestamp(int(submission['creationTimeSeconds']))
        submissionsDate = date(submissionsDate.year, submissionsDate.month, submissionsDate.day)
        pname = submission['problem']['name']
        verdict = submission['verdict']
        verdicts.add(verdict)
        # print((date.today()-submissionsDate).days)
        # print(submission)
        # print(pname, submissionsDate, verdict)
        
        if str(submissionsDate) not in mdict.keys():
            # print(submissionsDate)
            mdict[str(submissionsDate)]={}
        
        if verdict not in mdict[str(submissionsDate)].keys():
            # print(verdict)
            mdict[str(submissionsDate)][verdict]=[]

        # print()    
        mdict[str(submissionsDate)][verdict].append(pname)

    cnt=0
    for dat in mdict.keys():
        for verdict in mdict[dat].keys():
            mdict[dat][verdict] = len(set(mdict[dat][verdict]))
            if verdict=='OK':
                cnt+=mdict[dat][verdict]

    try:
        response = requests.get("https://codeforces.com/api/user.info?handles="+handle)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    state = response.json()['result']
    regDate = datetime.utcfromtimestamp(int(state[0]['registrationTimeSeconds']))
    regDate = date(regDate.year, regDate.month, regDate.day)

    tempDate = regDate
    # global finalData = {}
    finalData.clear()
    totaldays=1
    while tempDate<=date.today():
        # if(tempDate==regDate):
        # if tempDate not in mdict.keys():
        # print(mdict[str(tempDate)])
        finalData[str(tempDate)] = {}
        # else:
        for eachVerd in verdicts:
            if tempDate==regDate:
                if str(tempDate) not in mdict.keys():
                    finalData[str(tempDate)][eachVerd] = 0
                else:
                    if eachVerd not in mdict[str(tempDate)].keys():
                        finalData[str(tempDate)][eachVerd] = 0
                    else:
                        finalData[str(tempDate)][eachVerd] = mdict[str(tempDate)][eachVerd]
            else:
                if str(tempDate) not in mdict.keys():
                    finalData[str(tempDate)][eachVerd] = 0
                else:
                    if eachVerd not in mdict[str(tempDate)].keys():
                        finalData[str(tempDate)][eachVerd] = 0
                    else:
                        finalData[str(tempDate)][eachVerd] = mdict[str(tempDate)][eachVerd]

        tempDate = tempDate + timedelta(days=1)
    # return 
    # html.Center(
        # html.Div(children=[
    return [
            html.Br(),
            html.Center(html.H4("Pick A Date Range", className="text-success")),
            html.Center(dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=regDate,
                max_date_allowed=date.today()+timedelta(days=1),
                initial_visible_month=regDate,
                end_date=date.today()
            )),
            html.Br(),
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
                children=[html.Div(dcc.Graph(id='fig_avg'), style={'height':'100%'})], type="cube", fullscreen=False, debug=False, style={'position':'absolute', 'top':0})
            )        
    ]
    # ))

@app.callback(
    Output(component_id='loading_avg', component_property='children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('checklist', 'value')]
)
def update_output(start_date, end_date, value):
    if(start_date==None):
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
                        "text": "Please Pick the Start Date.",
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
    year, month, day = map(int, start_date.split('-'))
    date1 = date(year, month, day)

    year, month, day = map(int, end_date.split('-'))
    date2 = date(year, month, day)
    
    df = pd.DataFrame({'Date':[], 'Average':[]})

    pad=1
    sm=0
    while date1<=date2:
        for ve in verdicts:
            if ve in value:
                sm += (finalData[str(date1)][ve])
        df = df.append({'Date':str(date1), 'Average':sm/pad}, ignore_index=True)
        pad += 1
        date1 += timedelta(days=1) 

    # fig = go.Figure()
    fig = go.Figure(go.Scatter(
        x=list(df['Date']),
        y=list(df['Average']),
        # name='Average Accepted Submissions',
        # line=dict(color='royalblue', width=4, dash='dot')
        mode='lines+markers',
        hovertemplate="<i>When?</i>   <b>%{x}</b>"+"<br><b><i>Avg Submissions:</i></b> %{y:.2f}"
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
    Output('header1', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('my-id', 'value')]
)
def update_header(n_clicks, input_value):
    handle = input_value
    returndivs = []
    if input_value==None:
        return html.Div(id='header', className='card text-white bg-primary mb-3', style={'max-width':'20%','position':'absolute', 'top':0}, 
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
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        # html.Div(id='')
        return html.Div(id='header', className='card text-white bg-danger mb-3', style={'max-width':'20%','position':'absolute', 'top':0}, 
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
        return html.Div(id='header', className='card text-white bg-warning mb-3', style={'max-width':'20%','position':'absolute', 'top':0}, 
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
        return html.Div(id='header', className='card text-white bg-success mb-3', style={'max-width':'20%','position':'absolute', 'top':0}, 
                        children=[html.Div(
                                'Green Card',
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
                                    html.H4('Enjoy the stay', className='card-title'),
                                    html.P("The handle is being loaded. If it misses out anything from below, then press submit again because sometimes dash misbehaves.",className='card-text')
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

    return html.Center(html.Img(id="image_wc", src='data:image/png;base64,'+img2, style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'}))

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
