from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# data, heatmap
#df_crash = pd.read_csv(DATA_PATH.joinpath("test_data.csv"))
df_crash = pd.read_csv(DATA_PATH.joinpath("crashes_merged.csv"))

# data, barchart
df_crash_pivot = pd.pivot_table(df_crash,index=['Hour_of_the_week'],aggfunc=np.sum).reset_index()
#df_crash_pivot.reset_index(level=0, inplace=True)
# data, side barchart

# data, ratio
df_ratio = pd.read_csv(DATA_PATH.joinpath("PercentageMean.csv"))

colors = {
    'background': '#111111',
    'text': '#000000'
}

def plot_barchart(input_range=[0,168]):
    df_plot = df_crash_pivot[(df_crash_pivot['Hour_of_the_week']>input_range[0]) & (df_crash_pivot['Hour_of_the_week']<input_range[1])]
    fig_bar = px.bar(df_plot, x='Hour_of_the_week', y='Involved')
    fig_bar.update_layout(margin={"l":0,"r":0,"t":0,"b":0},height = 100)
    return fig_bar

def plot_heatmap(input_range=[0,168]):
    df_crashes_merged_plot = df_crash[(df_crash['Hour_of_the_week']>input_range[0]) & (df_crash['Hour_of_the_week']<input_range[1])]
    fig_map = px.density_mapbox(df_crashes_merged_plot, lat='LATITUDE', lon='LONGITUDE', z='Involved', radius=3,
    hover_data={'LATITUDE':False,'LONGITUDE':False,'Killed':True,'Injured':True, 'Time':True},
    center = {"lat": 40.730610, "lon": -73.935242}, zoom=9, mapbox_style="carto-positron")
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        font=dict(color='#737a8d'),
        coloraxis_showscale=False)
    return fig_map

def plot_chloropleth(input_range=[0,168]):
    df_ratio_plot = df_ratio[(df_ratio['hour_of_the_week']>input_range[0])&(df_ratio['hour_of_the_week']<input_range[1])].groupby("BOROUGH").mean().reset_index()
    df_ratio_plot['FIPS'] = df_ratio_plot['BOROUGH'].apply(lambda x: '36005' if x == "BRONX" else '36047' if x == "BROOKLYN" else '36061' if x == "MANHATTAN" else  '36081' if x == "QUEENS" else '36085' if x == "STATEN ISLAND" else "No Borough")
    fig_map_borough = px.choropleth_mapbox(df_ratio_plot, geojson=counties, locations='FIPS', color='Crash/Volume Ratio',
                           range_color=(min(df_ratio['Crash/Volume Ratio']),max(df_ratio['Crash/Volume Ratio'])),
                           mapbox_style="carto-positron",
                           zoom=9, center = {"lat": 40.730610, "lon": -73.935242},
                           opacity=0.5,
                           hover_data={'FIPS':False,'BOROUGH':True},
                           labels={'unemp':'unemployment rate'}
                          )
    fig_map_borough.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map_borough.update_coloraxes(colorbar_title=dict(text='',side='right'),
                                        colorbar=dict(len=0.9,xpad = 0, ypad = 0, x = 0.03, y = 0.5))
    return fig_map_borough


def plot_crash_borough(input_range=[0,168]):
    df_temp = df_ratio[(df_ratio['hour_of_the_week']>input_range[0]) & (df_ratio['hour_of_the_week']<input_range[1])]
    df_pivot = pd.pivot_table(df_temp,index=['BOROUGH'],aggfunc=np.sum).reset_index()
    fig_bar_crash = px.bar(df_pivot, x='BOROUGH', y='Percentage_Crash', title='Percentage Crashed')
    fig_bar_crash.update_layout(yaxis={'title': '','title_standoff':0,'side':'right'}, xaxis={'visible': False},
                                title={'text':"Percentage Crashed", 'x':0, 'y':0.98},titlefont_size = 12,
                                margin={"l":0,"r":0,"t":15,"b":0},height = 150)
    return fig_bar_crash

def plot_volume_borough(input_range=[0,168]):
    df_temp = df_ratio[(df_ratio['hour_of_the_week']>input_range[0]) & (df_ratio['hour_of_the_week']<input_range[1])]
    df_pivot = pd.pivot_table(df_temp,index=['BOROUGH'],aggfunc=np.sum).reset_index()
    fig_bar_volume = px.bar(df_pivot, x='BOROUGH', y='Percentage_Volume')
    fig_bar_volume.update_layout(yaxis={'title': '','title_standoff':0,'side':'right'}, xaxis={'visible': False},
                                title={'text':"Percentage Volume",  'x':0,'y':0.98},titlefont_size = 12,
                                margin={"l":0,"r":0,"t":15,"b":0},height = 150)
    return fig_bar_volume

def plot_ratio_borough(input_range=[0,168]):
    #df_temp = df_ratio[(df_ratio['hour_of_the_week']>input_range[0]) & (df_ratio['hour_of_the_week']<input_range[1])]
    df_temp = df_ratio[(df_ratio['hour_of_the_week']>input_range[0])&(df_ratio['hour_of_the_week']<input_range[1])].groupby("BOROUGH").mean()
    df_pivot = pd.pivot_table(df_temp,index=['BOROUGH'],aggfunc=np.sum).reset_index()
    fig_bar_ratio= px.bar(df_pivot, x='BOROUGH', y='Crash/Volume Ratio')
    fig_bar_ratio.update_layout(yaxis={'title': '','title_standoff':0,'side':'right'}, xaxis={'title': '','tickangle': 90},
                                title={'text':"Crash/Volume Ratio", 'x':0, 'y':0.99},titlefont_size = 12,
                                margin={"l":0,"r":0,"t":15,"b":10},height = 250)
    fig_bar_ratio.add_hline(y=1,line_dash="dot")
    return fig_bar_ratio



layout = dbc.Container([
    # MAP CHART
    #dcc.Graph(figure=fig_map),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                '''
                This collision map gives an overview of where the incidents occur.
                 Use the slider below to filter the data for specific timeframes during the hour of the week.
                 Change the map to display the ratio between volume and crashes across boroughs by using the dropdown to the right.
                ''',
                style={
                    'textAlign': 'left',
                    'color': colors['text']
                }
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Loading(
                    dcc.Graph(
                        id='mapchart',
                        figure={
                            "data": [], "layout": dict(plot_bgcolor="#FFFFFF")
                        }
                    )
                )
            ]),
            # SLIDER
            dcc.RangeSlider(id='hour_of_week_slider',
                min=0,
                max=168,
                step=1,
                value=[24, 72],
                marks={
                0: {'label': 'Monday', 'style': {'color': '#77b0b1'}},
                24: {'label': 'Tuesday'},
                48: {'label': 'Wednesday'},
                72: {'label': 'Thursday'},
                96: {'label': 'Friday'},
                120: {'label': 'Saturday'},
                144: {'label': 'Sunday'},
                },
                pushable=2
            ),

            # BAR CHART
            dcc.Loading(
                html.Div([
                    dcc.Graph(
                        id='barchart',
                        figure={
                            "data": [], "layout": dict(plot_bgcolor="#FFFFFF")
                        }
                        )
                ])
            )
        ],width=9),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id='map-graph-input',
                    options=[{'label': 'Collision Heatmap', 'value': 'Heatmap' },
                            {'label': 'Ratio Chloropleth', 'value': 'Chloropleth'}],
                    value='Heatmap',
                    placeholder="Type of graph"
                ),
                html.Br(),
                dcc.Loading(
                    dcc.Graph(
                        id='barchart-crash',
                        figure={"data": [], "layout": dict(plot_bgcolor="#FFFFFF")},
                        style={
                            'margin-left': 15,
                            'margin-right': 'auto',
                            'margin-top': 5,
                            'margin-bottom': 'auto',
                            'width': '100%'}
                    ),
                ),
                dcc.Loading(
                    dcc.Graph(
                        id='barchart-volume',
                        figure={"data": [], "layout": dict(plot_bgcolor="#FFFFFF")},
                        style={
                            'margin-left': 15,
                            'margin-right': 'auto',
                            'margin-top': 5,
                            'margin-bottom': 'auto',
                            'width': '100%'}
                    ),
                ),
                dcc.Loading(
                    dcc.Graph(
                        id='barchart-ratio',
                        figure={"data": [], "layout": dict(plot_bgcolor="#FFFFFF")},
                        style={
                            'margin-left': 15,
                            'margin-right': 'auto',
                            'margin-top': 5,
                            'margin-bottom': 0,
                            'width': '100%'}
                    ),
                ),
            ])
            #px.bar(df_test_pivot[0:5], x='Hour_of_the_week', y='Involved')
        ],width=3)
    ])
])


@app.callback(
    [
    Output('barchart','figure'),
    Output('mapchart','figure'),
    Output('barchart-crash','figure'),
    Output('barchart-volume','figure'),
    Output('barchart-ratio','figure')
    ],
    [
    Input('hour_of_week_slider','value'),
    Input('map-graph-input','value')
    ]
    #prevent_initial_call = True
)
def update_figures(slider_range, map_graph):
    fig_barchart = plot_barchart(slider_range)
    if map_graph == 'Heatmap':
        fig_map = plot_heatmap(slider_range)
    else: #Chloropleth
        fig_map = plot_chloropleth(slider_range)
    fig_bar_crash = plot_crash_borough(slider_range)
    fig_bar_volume = plot_volume_borough(slider_range)
    fig_bar_ratio = plot_ratio_borough(slider_range)
    return fig_barchart, fig_map, fig_bar_crash, fig_bar_volume, fig_bar_ratio