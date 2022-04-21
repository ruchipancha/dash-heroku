# essential imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

import plotly.express as px
import math
from dash import no_update

import pandas as pd
import numpy as np
import json

df_country_code = pd.read_csv("https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv")
df_country_code['Alpha-3 code'] = df_country_code['Alpha-3 code'].apply(lambda s : s.replace('"', ""))
display(df_country_code.head())

def get_country_name(country_code):    
  one_row = df_country_code[df_country_code['Alpha-3 code'].str.strip() == country_code]
  if not one_row.empty:
    display(one_row)
    return one_row['Country'].values[0]
  else:
    return ''

# import
# essential imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

import plotly.express as px
import math
from dash import no_update

import pandas as pd
import numpy as np
import json


# read primary data
df_country = pd.read_csv("https://raw.githubusercontent.com/smbillah/ist526/main/gapminder.csv")

# this is new
available_indicators = ['lifeExp',	'pop',	'gdpPercap']


# we load a secondary dataset with all countries and their 3-letter alpha code from github
df_country_code = pd.read_csv("https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv")
df_country_code['Alpha-3 code'] = df_country_code['Alpha-3 code'].apply(lambda s : s.replace('"', ""))

# a helper function
def get_country_name(country_code):    
  one_row = df_country_code[df_country_code['Alpha-3 code'].str.strip() == country_code]
  if not one_row.empty:
    display(one_row)
    return one_row['Country'].values[0]
  else:
    return ''
# end


# this css creates columns and row layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


## Uncomment the following line for runnning in Google Colab
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

## Uncomment the following line for running in a webbrowser
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # first row: header
    html.H4('A Sample Interactive Dashboard'),

    # second row: two drop-downs and radio-boxes. Each dropdown will take 4-column width
    html.Div([
      html.Div([
        dcc.Dropdown(
          id='xaxis-column',
          options=[{'label': i, 'value': i} for i in available_indicators], #e.g., {label: 'pop', 'value':'pop'}
          value='lifeExp'
        ),
        dcc.RadioItems(
          id='xaxis-type',
          options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
          value='Linear',
          labelStyle={'display': 'inline-block'}
        )
      ], className='four columns'),

      html.Div([
        dcc.Dropdown(
          id='yaxis-column',
          options=[{'label': i, 'value': i} for i in available_indicators],
          value='gdpPercap'
        ),
        dcc.RadioItems(
          id='yaxis-type',
          options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
          value='Linear',
          labelStyle={'display': 'inline-block'}
        )
      ], className='four columns')

    ], className='row'),


    # third row:
    html.Div([

      # first item: scatter plot
      html.Div([

        # add scatter plot
        dcc.Graph(
          id='scatter-graph',
          figure=px.scatter() # we'll create one inside update_figure function
        ),

        # add slider
        dcc.Slider(
          id='year-slider',
          min=df_country['year'].min(),
          max=df_country['year'].max(),
          value=df_country['year'].min(),
          marks={str(year): str(year) for year in df_country['year'].unique()},
          step=None
        )

      ], className='seven columns'),

      # second item: one blank column
      html.Div([
          html.Div(id='empty-div', children='')
      ], className='one column'),

      # third item: bar chart
      html.Div([
        dcc.Graph(
          id='bar-chart',
          figure=px.bar()
        )
      ], className='five columns')


    ], className = 'row'),

    # fourth row: debug message
    html.Div([
      html.H3('Debug'),
      #html.Br(),
      html.P(id='output_text_1', children='Total:'),
      html.P(id='output_text_2', children='Details:'),
      html.P(id='output_text_3', children='Conclusion:')
    ], className = 'row')

])

# callback definition
@app.callback(
  Output('scatter-graph', 'figure'),
  Output('output_text_1', 'children'), #debug
  Input('year-slider', 'value'),
  Input('xaxis-column', 'value'),
  Input('yaxis-column', 'value'),
  Input('xaxis-type', 'value'),
  Input('yaxis-type', 'value'),
)

# first callback function
def update_graph(selected_year, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type):
  # print all input params
  debug_params ='Input: {0}, {1}, {2}, {3}, {4}'.format(selected_year, xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type)

  # filter data frame by year
  filtered_df = df_country[df_country.year == selected_year]

  fig_scatter = px.scatter(
    data_frame = filtered_df,
    x=str(xaxis_column_name),
    y=str(yaxis_column_name),
    hover_name="country",
    color="continent",
    #size = 'pop',
    size_max=55,
    ### this is new --> adding a customdata that would be picked up during mouse hover
    custom_data = ["iso_alpha"],
    title= "{0}  vs {1} of Countries".format(xaxis_column_name, yaxis_column_name)
  )

  fig_scatter.update_layout(transition_duration=500)

  fig_scatter.update_xaxes(
    title=xaxis_column_name,
    type='linear' if xaxis_type == 'Linear' else 'log'
  )

  fig_scatter.update_yaxes(
    title=yaxis_column_name,
    type='linear' if yaxis_type == 'Linear' else 'log'
  )

  # return
  return fig_scatter, debug_params
# end update_

# second callback
@app.callback(
  Output('bar-chart', 'figure'),
  Output('output_text_2', 'children'), #debug
  Input('scatter-graph', 'clickData'), # hoverData
  Input('xaxis-column', 'value'),
  Input('xaxis-type', 'value')
)
# second callback definition
def update_bar_graph(clickData, xaxis_column_name, axis_type):
  if not clickData:
    return no_update

  debug_params ='Input: {0}, {1}, {2}'.format(clickData['points'], xaxis_column_name, axis_type)

  country_code = str(clickData['points'][0]['customdata'][0])

  filtered_df = df_country[df_country['iso_alpha'] == country_code]

  fig_bar = px.bar(
    data_frame = filtered_df,
    x="year",
    y=str(xaxis_column_name),
    title= "{0} of {1} in different year".format(xaxis_column_name, get_country_name(country_code))
  )

  fig_bar.update_yaxes(
    title=xaxis_column_name,
    type='linear' if axis_type == 'Linear' else 'log'
  )

  # return
  return fig_bar, debug_params

# end


# uncomment the following line to run in Google Colab
#app.run_server(mode='inline', port=8030)

# uncomment the following lines to run in Browser via command line/terminal
if __name__ == '__main__':
    app.run_server(debug=True)
