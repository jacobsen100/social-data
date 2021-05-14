from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pathlib
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import pandas as pd
import numpy as np
# Load data
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_age_sex = pd.read_csv(DATA_PATH.joinpath("df_age_sex.csv"))
injuryplot = pd.read_csv(DATA_PATH.joinpath("injuryplot.csv"))
#df_weather_plot = pd.read_csv(DATA_PATH.joinpath("df_weather_plot.csv"))
df_ratios = pd.read_csv(DATA_PATH.joinpath("PercentageMean.csv"))

weekday_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
github_link = 'https://github.com/jacobsen100/social-data'
notebook_link = 'https://github.com/jacobsen100/social-data'

colors = {
    'background': '#111111',
    'text': '#000000'
}

percentage_plot= (df_ratios.groupby('hour_of_the_week').sum()*100).reset_index().rename(columns={"Percentage_Crash":"Crash","Percentage_Volume":"Volume"})
fig = px.line(percentage_plot, x="hour_of_the_week", y=["Crash",'Volume'],
             title="Crash and Volume ratio throughout the week",labels={"variable": ""},)
fig.update_layout(xaxis = dict(tickvals = np.linspace(1,168-24,7), ticktext = weekday_list),
                xaxis_title='Days',yaxis_title="%",title={'x':0.5, 'xanchor': 'center'},)


# Plotting the number of crashes for every sex dependent on ange
fig1 = px.line(df_age_sex, x="PERSON_AGE", y="Crashes", color='PERSON_SEX', 
            title="Crashes dependent on age and gender",labels={"PERSON_SEX": ""})
fig1.update_layout(xaxis_title="Age",title={'x':0.5, 'xanchor': 'center'})


data = [
    go.Scatter(x = injuryplot['Year'], y=injuryplot["NUMBER OF PERSONS INJURED"], name='Injured'),
    go.Scatter(x = injuryplot['Year'], y=injuryplot["NUMBER OF PERSONS KILLED"], name='Killed', yaxis='y2')]
# settings for the new y axis
y1 = go.YAxis(title='Injured', titlefont=go.Font(color='Blue'))
y2 = go.YAxis(title= 'Killed', titlefont=go.Font(color='Red'))
y2.update(overlaying='y', side='right')
# adding the second y axis
layout = go.Layout(yaxis1 = y1, yaxis2 = y2)
fig2 = go.Figure(data=data, layout=layout)
fig2.update_layout( title={'text':"Number of killed and injured persons",'x':0.5, 'xanchor': 'center'},xaxis_title='Year')


fig3 = px.line(df_ratios, x="hour_of_the_week", y="Crash/Volume Ratio", color="BOROUGH", title="Crash/Volume Ratio for every Borough")
fig3.update_layout(xaxis = dict(tickvals = np.linspace(1,167-24,7),ticktext = weekday_list),
        xaxis_title='Week days',yaxis_title="Crash/Volume Ratio",title={'x':0.5, 'xanchor': 'center'})


### PAGE ###
layout= html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1("Welcome!"),width=4),
        dbc.Col([html.Div(dcc.Link("Github", href=github_link),style={'display': 'inline-block'}),
                html.A([html.Img(src=app.get_asset_url("GitHub-Mark-32px.png"),
                            style={'height':'32px', 'width':'32px',"margin-left":"5px"})
                        ],href= github_link),       
                html.Div(dcc.Link("Notebook", href=github_link),style={'display': 'inline-block',"margin-left":"15px"}),
                html.A([html.Img(src=app.get_asset_url("JupyterNotebook-64px.png"),
                            style={'height':'32px', 'width':'32px',"margin-left":"5px"})
                        ],href= notebook_link)       
                ],width=4,style={"margin-top":"5px"}
        ),
            ],justify="between",
        ),
    dcc.Markdown(
    '''
        You have just entered the webpage that will explain various aspects of collisions in New York City.
        The primary goal of this webpage is to facilitate a platform which enables a
        broad and detailed overview of the collision patterns in New York City.
        The webpage is divided into three different tabs displayed at the top. The current tab contains summary statistics regarding
        time, gender and borough. The second tab, Collision Maps, contains two different geographical plots in which information
        about single collisions and collision patterns specified by the time of interest can be obtained. Lastly, in the Predict Severity tab
        a model to predict the severity of your injuries in the case of you being a crash-victim based on various demographic and geographical inputs 
        can be found.
    '''),
    html.H1("Total volume and collisions"),
    dcc.Markdown(
    '''
        The plot shows that the volume and crash percentages follow each other quie well.
        In the weekdays, the volume has two peak points, one at the morning rush hour and one at the afternoon rush hour. 
        This makes good sense, as this is the time where the traffic is affected by people going to and home from work.
        The pattern is a little different at the weekend, as there is only one peak point in the afternoon, as this is the 
        time people are going out to enjoy the city. The volume are also a bit lower at the weekend, due to fewer people are
        going to work. The same patterns are seen in the crashes, however, the crashes has some higher peak points. 
        This shows that there is relative more crashes compared to the traffic volume at the peak points, and vice versa at 
        the other times of the day. The biggest difference between volume and crash percentages is found at sunday morning around 6 AM.
        Here, the percentage of the total crashes is nearly twice as high as the total volume. 
    '''),
    dcc.Graph(figure=fig),
    html.H1("Boroughs"),
    dcc.Markdown(
    '''
        The ratio is clearly on a different level between all the boroughs.
        Brooklyn seems to be the most dangerous place, while Staten Island is the safest,
        as their ratio is respectively above and below the others boroughs in the entire week.
        The most dangerous time to drive in the whole week is in Brooklyn at 5 AM, with a ratio of around 3.5, thus 3.5 times more
        crashes compared to the traffic.
        It is also noticed that all the borougs has the same patterns, as all are having peaks at night or early morning.
        A reason for this could be that the volume is rather low at this point,
        thus crashes has an great impact in the ratio. Furthermore, drunk driving and people being tired in the middle of the 
        night are also factors that could increase the number of crashes compared to the volume. 
    '''),
    dcc.Graph(figure=fig3),
    html.H1("Gender and age"),
    dcc.Markdown('''
        The plot shows that the number of crashes is on a steady level in the range between 0 to 16.
        From the age of 16, a person is allowed to have a driving license, which is clearly seen in the plot. 
        The number of crashes has an increasing trend from this point and until the person is 30 years old, 
        which is the peak point for the genders. The reason for this trend could be that the drivers are young and unexperienced,
        thus being involved in more crashes. From the age of 30, the trend is decreasing, indicating that the persons are getting
        more responsible in the traffic.
    ''') ,
    dcc.Graph(figure=fig1),
    html.H1("Severity of crashes over timer"),
    dcc.Markdown(
    '''
        The plot consists of two y-axes due to the difference in scale, thus the left y-axis shows the number of injured persons,
        while the right shows the number of killed persons. 
        The plot shows that the number of injured and killed persons
        involved in a crash has more or less the same trend from 2013 to 2017, with some minor deviations. The recent trend is that the number of
        injured persons decreases, while the number of killed person increases. The number of injured persons dropped with around
        30% from 2019 to 2020, which could be an effect from corona. However, the number of killed persons 
        are acutally at the second highest level in 2020, thus not being effected in the same way.
    '''),
    dcc.Graph(figure=fig2),
    ],
    style={ 'Align': 'center',
            'color': colors['text'],
            'margin-left': 'auto',
            'margin-right': 'auto',
            'width': '70%'}
)