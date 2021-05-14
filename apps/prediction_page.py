from app import app
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

import pathlib
import joblib
import pandas as pd
import numpy as np

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
random_forest_model = joblib.load(open(DATA_PATH.joinpath('random_forest.pkl'), 'rb'))

colors = {
    'background': '#111111',
    'text': '#000000'
}

age_list = ['<16','17-25','26-35','36-45','46-55','56-65','65<']
weekday_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
borough_list = ['Queens', 'Bronx', 'Brooklyn', 'Manhattan', 'Staten Island']
weather_list = ['Fog','Snow','Rain']
transportation_list = ['Pedestrian','Occupant','Bicyclist']
gender_list = ['Male','Female','Undefined']

def input_interpreter(age,weather,borough,hour,day,gender,transportation):
    age_vec = [age==ele for ele in age_list]
    weather_vec = [weather==ele for ele in weather_list]
    borough_vec = [borough==ele for ele in borough_list]
    hour_of_week = [24*weekday_list.index(day)+hour]
    gender_vec = [gender==ele for ele in gender_list]
    transport_vec = [transportation==ele for ele in transportation_list]
    return age_vec + hour_of_week + weather_vec + borough_vec + gender_vec + transport_vec

def plot_pred(pred):
    arr= random_forest_model.predict_proba(pred)
    arr1=pd.DataFrame(arr)
    arr1=arr1.rename(columns = {0: 'Injured', 1: 'Unharmed'},index = {0: 'Prediction'})

    fig_pred = px.bar(arr1,color_discrete_sequence=["red", "green"],orientation='h',height=100)
    fig_pred.update_layout(
        title={'text':"Probaility of prediction", 'x': 0.01, 'yanchor':'top'},titlefont_size = 12,
        xaxis={'title': '', 'range': [0, 1]},yaxis={'visible':False},
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        margin={"l":0,"r":0,"t":5,"b":0},
        legend=dict(title='', orientation="h",
        yanchor="bottom",y=1.02,
        xanchor="right", x=1))
    return fig_pred

def plot_empty():
    fig_empty = px.bar()
    fig_empty.update_layout(yaxis={'visible':False},xaxis={'visible':False},
                            paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig_empty

# Factor plot
X=[0.1481278013419531,
 0.01061177767783488,0.018804984944237223,0.003118748411317166,
 0.001864274774334416,0.004424122645384432,0.009518328755189993,0.0051538034149707325,0.0015930590967027267,
 0.11996540233611055,0.14108736742822617,0.07908183114084827,
 0.035704731848722034,0.22525009631906137,0.07670165564533155,
 0.00981014588347008,0.016712524384863228,0.007862518751796905,0.07514621145480652,0.004294941760222177,0.003152701985192842,0.002012969999423749]
Y=['Time of the week',
 'Fog','Rain','Snow',
 'Bronx','Brooklyn','Manhattan','Queens','Staten Island',
 'Female','Male','Undefined',
 'Bicyclist','Occupant','Pedestrian',
 '0-16','17-25','26-35','36-45','46-55','56-65','65+']
df_model_factors = pd.concat([pd.Series(X, name="Effect"), pd.Series(Y,name="Factor")], axis=1)
fig_bar_factors = px.bar(df_model_factors, x='Effect', y='Factor')
fig_bar_factors.update_layout(yaxis={'title': '','title_standoff':0},margin={"l":0,"r":0,"t":0,"b":0})

### PAGE ###
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            ### Headers
                dcc.Markdown(
                    '''
                    On the left is a model that predicts whether a crash causes injuries or not.
                    Input values in all the dropdowns, press predict and the model will return the severity of the crash along
                    with the models certainty.\
                    On the right hand side is a plot over which factors have the most affect on the outcome of the crash.
                        ''',
                    style={
                        'textAlign': 'left',
                        'color': colors['text']
                    }
                ),
                #html.Br()
        ]),
    ]),

    dbc.Row([
        dbc.Col(children=[
            ### Dropdowns
            html.Div([
                html.Div([
                    # GENDER
                    html.Div([
                        dcc.Dropdown(
                            id='gender-input',
                            options = [{'label': i, 'value': i} for i in gender_list],
                            placeholder="Gender"
                        ),
                    ],
                    ),

                    # AGE
                    html.Div([
                        dcc.Dropdown(
                            id='age-input',
                            options=[{'label': i, 'value': i} for i in age_list],
                            placeholder="Age"
                        ),
                    ], 
                    ),

                    # WEATHER
                    html.Div([
                        dcc.Dropdown(
                            id='weather-input',
                            options=[{'label': i, 'value': i} for i in weather_list+['Clear']],
                            placeholder="Weather"
                        ),
                    ], 
                    ),
                    
                    # BOROUGH
                    html.Div([
                        dcc.Dropdown(
                            id='borough-input',
                            options=[{'label': i, 'value': i} for i in borough_list],
                            placeholder="Borough"
                        ),
                    ], 
                    ),
                    # HOUR
                    html.Div([
                        dcc.Dropdown(
                            id='hour-input',
                            options=[{'label': str(i)+":00", 'value': i} if i>9 else {'label': "0"+str(i)+":00", 'value': i} for i in range(24)],
                            placeholder="Hour"
                        ),
                    ],
                    ),

                    # DAY
                    html.Div([
                        dcc.Dropdown(
                            id='day-input',
                            options=[{'label': i, 'value': i} for i in weekday_list],
                            placeholder="Day"
                        ),
                    ], 
                    ),

                    # TRANSPORT
                    html.Div([
                        dcc.Dropdown(
                            id='transport-input',
                            options=[{'label': i, 'value': i} for i in transportation_list],
                            placeholder="Transportation"
                        ),
                    ], 
                    )

                    ], style={
                        'borderBottom': 'thin lightgrey solid',
                        'backgroundColor': 'rgb(250, 250, 250)',
                        'padding': '10px 10px'}
                    )
            ]),
            html.Br(),
            # PREDICT
            html.Div([
                html.Button('Predict', id='predict-button'),
                html.Span(id="predict-output", style={"vertical-align": "middle", 'margin-left': '10px'}),

            ], style={'margin-bottom': '10px',
                    'textAlign':'center',
                    'width': '50%',
                    'margin':'auto'}
            ),
            
            dcc.Graph(
                        id='fig_pred',
                        figure={"data": [], 
                                "layout": dict( xaxis={'visible':False},yaxis={'visible':False},
                                                paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')},
                        style={
                            'margin-left': 'auto',
                            'margin-right': 'auto',
                            'margin-top': 'auto',
                            'margin-bottom': 'auto',
                            'width': '100%'}
                    ),

            ],
            width=5
        ),
        dbc.Col([
            dcc.Graph(figure=fig_bar_factors,
                    style={
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'margin-top': 'auto',
                        'margin-bottom': 'auto',
                        'width': '100%'
                    })
            ],width=7
        ),
    ],justify="start",
    ),
])

@app.callback(
    [
    Output(component_id="predict-output", component_property="children"),
    Output(component_id="fig_pred", component_property="figure")
    ], 
    [Input("predict-button", "n_clicks")],
    [
    State(component_id="age-input", component_property="value"),
    State(component_id="hour-input", component_property="value"),
    State(component_id="day-input", component_property="value"),
    State(component_id="weather-input", component_property="value"),
    State(component_id="borough-input", component_property="value"),
    State(component_id="gender-input", component_property="value"),
    State(component_id="transport-input", component_property="value")
    ],
    prevent_initial_call = True
)
#, weather, borough, gender, transport
def update_result(click, age, hour, day, weather, borough, gender, transport):
    if None in [click, age, hour, day, weather, borough, gender, transport]:
        fig_pred = plot_empty()
        return "Please insert a value in all the inputs", fig_pred
    else:
        fig_pred = plot_pred([input_interpreter(age, weather, borough, hour, day, gender, transport)])
        return random_forest_model.predict([input_interpreter(age, weather, borough, hour, day, gender, transport)])[0], fig_pred