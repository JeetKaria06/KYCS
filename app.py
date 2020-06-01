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


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.DARKLY]

colors = {
    'background': '#222',
    'text': '#fff',
    'warn': '#FFFF00',
    'dimInput': '#696969'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
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
    html.Center(html.Div(className='badge badge-danger',id="my-div", children='')),
    html.Br(),
    html.H3(
        children='Submission Distribution Verdictwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Graph(id='fig0'),
    html.Br(),
    html.H3(
        children='Submission Distribution Verdict+Ratingwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Graph(id='fig'),
    html.Br(),
        html.H3(
        children='Submission Distribution Tags+Verdictwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Graph(id='fig-1'),
    html.Br(),
    html.H3(
        children='Submission Distribution Tags+Verdict+Ratingwise',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    dcc.Graph(id='fig1'),
    html.Br(),
    html.H3(
        children='WordClound of the tags based on your Submissions',
        style={
            'textAlign': 'center'
        },
        className="text-info"
    ),
    html.Br(),
    html.Center(html.Img(id="image_wc", style={'height':'50%', 'width':'50%', 'marginRight':'auto', 'marginLeft':'auto'})),
    html.Br(),
    html.Br(),
    html.Center(
        html.Div(
            className='jumbotron',
            children=[
                html.H1('developed by [ Jeet_Karia ]'),
                html.Br(),
                dbc.Button('GitHub', id='gb', className="btn btn-primary btn-lg", href='https://github.com/JeetKaria06', style={'max-width':'15%'}),
                dbc.Button('LinkedIN', id='ln', className="btn btn-primary btn-lg", href='https://www.linkedin.com/in/jeet-karia-628773170/', style={'max-width':'15%', 'backgroundColor':'#0072b1'}),
                dbc.Button('Instagram', id='ig', className="btn btn-primary btn-lg", href='https://www.instagram.com/karia_jeet/', style={'max-width':'15%', 'backgroundColor':'#bc2a8d'})
            ]
        )
    )
])
])

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
    Output('image_wc', 'src'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_wc(n_clicks, input_value):
    handle=input_value
    if handle==None:
        return ''
    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return ""

    if(response.status_code==400):
        return ""
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

    return 'data:image/png;base64,'+img2

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='fig0', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_output_die(n_clicks, input_value):  # Only Verdict wise
    handle = input_value
    if handle==None:
        return {
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

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return {
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

    if(response.status_code==400):
        return {
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
    return fig

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='fig-1', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_output_div(n_clicks, input_value):       # tag and verdict combined
    handle = input_value
    if handle==None:
        return {
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

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return {
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

    if(response.status_code==400):
        return {
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
    return fig

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='fig1', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
    # [dash.dependencies.State(component_id='figures', component_property='children')]

)
def update_output_diven(n_clicks, input_value):       # tag, verdict and rating combined
    handle = input_value

    if handle==None:
        return {
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

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return {
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

    if(response.status_code==400):
        return {
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
    return fig

@app.callback(
    # Output(component_id='my-div', component_property='children'),
    Output(component_id='fig', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_output_dive(n_clicks, input_value):             # Verdict and Rating combined
    handle = input_value

    if handle==None:
        return {
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

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return {
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

    if(response.status_code==400):
        return {
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
    return fig
@app.callback(
    Output(component_id='my-div', component_property='children'),
    # Output(component_id='fig1', component_property='figure'),
    [Input(component_id='submit-val', component_property='n_clicks')],
    [dash.dependencies.State(component_id='my-id', component_property='value')]
)
def update_output(n_clicks, input_value):               # Valid User
    handle = input_value
    
    if handle==None:
        return "Enter the Handle :|"    

    try:
        response = requests.get("https://codeforces.com/api/user.status?handle="+handle+"&from=1")
    except requests.exceptions.RequestException as e:
        return "Host Didn't responded!"    

    if(response.status_code==400):
        return("No such user exists :( ")
        # exit()
    else:
        return("Handle is being loaded.")

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
