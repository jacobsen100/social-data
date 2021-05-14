import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import map_page, prediction_page,blog_page


button_style = {
  'background-color': '#d0e1f5',
  #'border': None,
  'color': 'white',
  'height':'100px',
  #'width':'25%',
  'width':'100%',
  'padding': '5px 32px',
  'text-align': 'center',
  #'text-decoration': None,
  'display': 'inline-block',
  'font-size': '16px'
}


# Defines the page
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Link(html.Button('Frontpage',style=button_style), href='/apps/blog_page')),
        dbc.Col(dcc.Link(html.Button('Collision map',style=button_style), href='/apps/map_page')),
        dbc.Col(dcc.Link(html.Button('Predict severity',style=button_style), href='/apps/prediction_page'))
    ],no_gutters=False),
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url', refresh=False),
            #html.Br(),
            html.Div(id='page-content', children=[]) # All page link are going into this childrens argument
        ])
    ])
])


@app.callback(Output(component_id='page-content', component_property='children'),
              [Input(component_id='url', component_property='pathname')])

# Remember to add here if another page is added
def display_page(pathname):
    if pathname == '/apps/map_page':
        return map_page.layout
    if pathname == '/apps/prediction_page':
        return prediction_page.layout
    if pathname == '/apps/blog_page':
        return blog_page.layout
    else:
        return blog_page.layout
        #return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True,port=8051)