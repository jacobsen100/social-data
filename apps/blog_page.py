from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pathlib

import pandas as pd
import numpy as np
# Load data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_crash = pd.read_csv(DATA_PATH.joinpath("test_data.csv"))
df_crash_pivot = pd.pivot_table(df_crash,index=['Hour_of_the_week'],aggfunc=np.sum)
df_crash_pivot.reset_index(level=0, inplace=True)


# Construct figure
fig_bar_test = px.bar(df_crash_pivot, x='Hour_of_the_week', y='Involved')
fig_bar_test.update_layout(margin={"l":0,"r":0,"t":0,"b":0}, height = 100)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


### PAGE ###
layout = html.Div([
    dcc.Markdown(
    '''
    # Headline?
    *This text will be italic*

    _This will also be italic_
    asfa af

    **This text will be bold**

    __This will also be bold__

    _You **can** combine them_
    '''
    ),
    
    dcc.Graph(figure=fig_bar_test),
    dcc.Markdown(
        '''
        # Titel 1
        The plot shows that the volume and crash percentages follow each other quie well. 
        In the weekdays, the volume has two peak points, at the morning and afternoon rush hour. 
        This makes good sense, as this is the time where the traffic is affected by people going to and home from work. 
        The pattern is a little different at the weekend, as there is only one peak point in the afternoon, as this is 
        the time people are going out to enjoy the city. The volume are also a bit lower at the weekend, due to fewer 
        people are going to work. The same patterns are seen in the crashes, however, the crashes has some higher peak points. 
        This shows that there is relative more crashes compared to the traffic volume at the peak points, and vice versa at 
        the other times of the day. Next, the number of crashes for the different boroughs will be investigated.
        '''
    ),
    dcc.Graph(figure=fig_bar_test),
    dcc.Markdown('''
    ewe'''),
    dcc.Markdown(
        '''
        # Titel 2
        The plot shows that the number of crashes is on a steady level in the range between 0 to 16. 
        From the age of 16, a person is allowed to have a driving license, which is clearly seen in the plot. 
        The number of crashes has an increasing trend from this point and until the person is 30 years old, which is 
        the peak point for the genders. The reason for this trend could be that the drivers are young and unexperienced, 
        thus being involved in more crashes. After the peak point, the number of crashes are decreasing in the entire period of time.
        ewe'''
    ),
    
    dcc.Graph(figure=fig_bar_test),
    dcc.Markdown(
        '''
        # Titel 3
        The plot consists of two y-axis due to the difference in scale, thus the left shows the number of injured persons, 
        while the right shows the number of killed persons. The plot shows that the number og injured and killed persons 
        involved in a crash has more or less the same trend, with some minor deviations. 
        The previously mentioned effect from corona is seen in the number of injured persons, as this is at the lowest 
        level in the entire period. The number of killed persons, however, are acutally at the second highest level in 2020, 
        thus not being effected by the lower number of crashes. The next part will investigate how the time of the day affects 
        the number of crashes, starting by plotting the crashes depending time of the day.
        '''
    ),
    
    dcc.Graph(figure=fig_bar_test),
   
   
    
],
style={
            'Align': 'center',
            'color': colors['text'],
            'margin-left': 'auto',
            'margin-right': 'auto',
            'width': '70%'
        }
)
