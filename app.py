import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does
from whitenoise import WhiteNoise   #for serving static files on Heroku

# my header
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Instantiate dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY]) 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df_country = pd.read_csv("https://raw.githubusercontent.com/smbillah/ist526/main/gapminder.csv")

fig_yearpop = px.bar(data_frame = df_country, 
    x="continent",        # continent
    y="pop",              # population    
    color="continent",    # group/label

    range_y=[0, 8000000000],
    title= "Population of Countries", 
)

app.layout = html.Div([
  # first row: header
  html.H1('In Class Activity'),

  # second row: <scratter-plot> <empty> <bar chart> 

  html.Div([
         html.Div([
           html.Div([dcc.Graph(
               id="scatter-plot",
               figure = fig_yearpop
            ),
           ],className = "ten columns"),
           html.Div([
                  html.H3('Filter'),   
                  html.Br(),
                  html.H4('Select'),
                  dcc.RadioItems(["Red","Blue"]),
                  html.Br(),
                  html.H4('Slide'),
                  dcc.Slider(0, 20, 5,
                      value=10,
                      id='my-slider'
                  ),
           ], className = "two columns"),

         ], className = "twelve columns"),   
  ], className = "row"), 



  html.Div([
    html.Div([
      dcc.Graph(
          id = 'year-bar',
          figure = px.bar()
      )
    ], className = 'four columns'),
    html.Div([
              dcc.Dropdown(),
              html.Br(),
              html.H3("Graph summary")
    ], className = 'two columns'),
    html.Div([
          dcc.Graph(
          id = 'world-map',
          figure = px.bar()
      )
    ], className = 'four columns'),
    html.Div([
      html.H3('Summary'),
      html.Br(),
      html.H4(id='output_text_1', children='Total:'),
      html.H4(id='output_text_2', children='Details:'),
      html.H4(id='output_text_3', children='Conclusion:')
    ], className = 'two columns'),
  ], className = 'row')
])
# Run dash app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)
 
