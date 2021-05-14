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
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_age_sex = pd.read_csv(DATA_PATH.joinpath("df_age_sex.csv"))
injuryplot = pd.read_csv(DATA_PATH.joinpath("injuryplot.csv"))

df_ratios = pd.read_csv(DATA_PATH.joinpath("PercentageMean.csv"))

weekday_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
github_link = 'https://github.com/jacobsen100/social-data'
notebook_link = 'https://github.com/jacobsen100/social-data/blob/main/jupyter-notebook/Explainer_Notebook_Final_ipynb.ipynb'

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
fig3.update_layout(xaxis = dict(tickvals = np.linspace(1,167-24,7),ticktext = weekday_list),legend=dict(title=''),
        xaxis_title='Week days',yaxis_title="Crash/Volume Ratio",title={'x':0.5, 'xanchor': 'center'})


### PAGE ###
layout= html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1("NYC Collisions"),width=6),
        dbc.Col([html.Div("Github",style={'display': 'inline-block'}),
                html.A([html.Img(src=app.get_asset_url("GitHub-Mark-32px.png"),
                            style={'height':'32px', 'width':'32px',"margin-left":"5px"})
                        ],href= github_link),       
                html.Div("Notebook",style={'display': 'inline-block',"margin-left":"15px"}),
                html.A([html.Img(src=app.get_asset_url("JupyterNotebook-64px.png"),
                            style={'height':'32px', 'width':'32px',"margin-left":"5px"})
                        ],href= notebook_link)       
                ],width=4,style={"margin-top":"5px"}
        ),
            ],justify="between",
        ),
    dcc.Markdown(
    '''
        Welcome. You have just entered the webpage that will explain various aspects of collisions in New York City.
        The associated github and notebook can be accessed by the icons above.
        The primary goal of this webpage is to facilitate a platform that enables a
        broad and detailed overview of the collision patterns in New York City. It has been created primarly with NYC Deparment of Transportation in mind, 
        as it is belived they are the ones who could benefit the most from its insights of focal points of interest regarding crash vs. traffic-volume. 
        The platform is also suitable for the public who seek to gain insights about collisions in New York.
        The webpage is divided into three different tabs displayed at the top, each contributing with a part of the storytelling
        regarding the collisions. The current tab contains visualisations which purpose is to reveal collision
        patterns regarding time, gender and borough. By pressing on the second tab "Collision maps", two different geographical plots
        will be available. The first provides detailed information about sppecific crash-sites with a heatmap, while the second shows the crash/volume
        ratio between the boroughs, both specified by the desired range of time. In the last tab "Predict Severity",
        a model to predict the severity of your injuries in the case of you being a crash victim based on various demographic and external inputs 
        can be found.
    '''),
    html.H1("Total volume and collisions"),
    dcc.Markdown(
    '''
        The plot below shows that the traffic volume and crash ratio follow each other quite well.
        On the weekdays, the volume has two peak points, one at the morning rush hour and one at the afternoon rush hour. 
        This makes good sense, as this is the time where the traffic is affected by people going to and home from work.
        The pattern is a little different at the weekend, as there is only one peak point in the afternoon, as it is belived it is the 
        time people are going out to enjoy the city. The trafic volume is also a bit lower at the weekend, due to fewer people
        going to work. The same patterns are seen in the crashes, however, the crashes have some higher peak points. 
        This shows that there are relatively more crashes compared to the traffic volume at the peak points, and vice versa at 
        the other times of the day. The biggest difference between traffic volume and crash percentages is found on Sunday morning around 6 AM.
        Here, the percentage of the total crashes is nearly twice as large as the total volume, thus being the most dangerous time to be
        in the traffic
    '''),
    dcc.Graph(figure=fig),
    html.H1("Boroughs"),
    dcc.Markdown(
    '''
        Below plot shows that the ratio is on different levels between all the boroughs.
        Brooklyn is the most dangerous borough, while Staten Island is the safest,
        as their ratio is respectively above and below the other boroughs in the entire week.
        The most dangerous time to drive in the whole week is in Brooklyn at 5 AM, with a ratio of around 3.5.
        It is also noticed that all the boroughs have the same patterns, as all are having peaks at night or early morning.
        A reason for this could be that the volume is rather low at this point, thus crashes has a great impact on the ratio.
        Furthermore, drunk driving and people being tired in the middle of the 
        night are also factors that could increase the number of crashes compared to the volume
    '''),
    dcc.Graph(figure=fig3),
    html.H1("Gender and age"),
    dcc.Markdown('''
        The below plot shows that the number of crashes is on a steady level in the age-range between 0 to 16.
        From the age of 16, a person is allowed to have a driving license, which is clearly seen in the plot. 
        The number of crashes has an increasing trend from this point and until the person is 30 years old, 
        which is the peak point for the both gender. The reason for this trend could be that the drivers are young and inexperienced,
        thus being involved in more crashes. From the age of 30, the trend is decreasing, indicating that the persons are getting
        more responsible in the traffic
    ''') ,
    dcc.Graph(figure=fig1),
    html.H1("Severity of crashes over timer"),
    dcc.Markdown(
    '''
        The below plot consists of two y-axes due to the difference in scale, thus the left y-axis shows the number of injured persons,
        while the right shows the number of killed persons in crashes. 
        The plot shows that the number of injured and killed persons
        involved in a crash has more or less the same trend from 2013 to 2017, with some minor deviations. The recent trend is that the number of
        injured persons decreases, while the number of killed person increases. The number of injured persons dropped by around
        30% from 2019 to 2020, which could be an effect of the Coronavirus. However, the number of killed persons 
        is at the second-highest level in 2020, thus not being affected the same way
    '''),
    dcc.Graph(figure=fig2),
    html.H1("Summary"),
    dcc.Markdown('''
     The key findings from the visualisations are that Brooklyn has the highest crash/volume ratio while Staten Island has the lowest. 
     On this basis, it is recommended to the NYC Department of Transportation to take inspirations from the infrastructure in Staten Island 
     and implement this in Brooklyn, if possible. Furthermore, the crash/volume ratio has its peak in all of the boroughs on Sunday morning,
     which means it can be recommended to the NYC Department of Transportation to be specifically aware of this time-frame.  
     Another impact area could be to target a campaign towards persons between 16 and 30 regarding traffic safety, 
     due to the rapid increase in collisions for this age group.
     It could be interesting to investigate the reason for this trend, and hereby prepare solution-oriented proposals.
     
     **Now that you have finished reading the front page, we recommend you to browse the two next tabs to explore more insights about collisions in New York.**
     '''
    )
    ],
    style={ 'Align': 'center',
            'color': colors['text'],
            'margin-left': 'auto',
            'margin-right': 'auto',
            'width': '70%'}
)