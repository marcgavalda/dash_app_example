
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server=app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df= pd.read_csv('nama_10_gdp_1_Data.csv')
df = df.drop(df[df.GEO.isin(["European Union (current composition)",
                    "European Union (without United Kingdom)",
                    "European Union (15 countries)",
                    "Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)",
                    "Euro area (19 countries)",
                    "Euro area (12 countries)"])].index)

df= df.drop(columns=['Flag and Footnotes'])
df= df.drop(df[df.Value.isin([':'])].index) 

available_indicators = df['NA_ITEM'].unique()
available_country = df['GEO'].unique()
available_unit=df['UNIT'].unique()

app.layout = html.Div([
    html.H1('My first project: Indicators',style={'textAlign': 'center'}),
    html.H2('Cecilia Montessoro',style={'textAlign': 'center', 'color': 'blue'}),
    html.H3('Figure 1',style={'textAlign': 'center', 'size': 20,'color': 'red'}),
    html.Div([
        html.Div([
            html.Label('Select Indicator for X axis'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            html.Div(style={'height': 10, 'display': 'inline-block'}),
            html.Label('Select Unit Mesure'),
            dcc.Dropdown(
                id='unit',
                options=[{'label': i, 'value': i} for i in available_unit],
                value="Current prices, million euro",
                style={'width': '90%'})
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Select Indicator for Y axis'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            
            html.Div(style={'height': 10, 'display': 'inline-block'}),
            
            dcc.RadioItems(
                id='axis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    html.Div(style={'height': 15, 'display': 'inline-block'}),
    
    dcc.Graph(id='indicator-graphic'),
    
    html.Div(style={'height': 30, 'display': 'inline-block'}),
    
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(TIME): str(TIME) for TIME in df['TIME'].unique()},
        ), 
    html.Div(style={'height': 80, 'display': 'inline-block'}),
    
#SECOND PART LAYOUT 
    html.H3('Figure 2', style={'textAlign': 'center', 'size': 20,'color': 'red'}),
    html.Div([
        html.Div([
            html.Label('Select Indicator'),
            dcc.Dropdown(
                id='yaxis_column_2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            
            html.Div(style={'height': 10, 'display': 'inline-block'}),
            html.Label('Select Unit Mesure'),
            dcc.Dropdown(
                id='unit_2',
                options=[{'label': i, 'value': i} for i in available_unit],
                value="Current prices, million euro",
                style={'width': '90%'})
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Select Country'),
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_country],
                value="Belgium"
            ),
            html.Div(style={'height': 10, 'display': 'inline-block'}),
            dcc.RadioItems(
                id='axis_type_2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear'
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})       
    ]),
    html.Div(style={'height': 15, 'display': 'inline-block'}),
    dcc.Graph(id='indicator_graphic_country')

])


# FIRST GRAPH 

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('axis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('unit', 'value')])
    
def update_graph(xaxis_column_name, yaxis_column_name, 
                 axis_type,year_value,unit):
    dff = df[df['TIME'] == year_value]
    dfff= dff[dff['UNIT']==unit]
    
    return {
        'data': [go.Scatter(
            x=dfff[(dfff['NA_ITEM'] == xaxis_column_name) & (dfff['GEO']== i)]['Value'],
            y=dfff[(dfff['NA_ITEM'] == yaxis_column_name) & (dfff['GEO']== i)]['Value'],
            text=dfff[(dfff['NA_ITEM'] == yaxis_column_name) & (dfff['GEO']== i)]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i[:15]) 
                 for i in df.GEO.unique()
        ],
        'layout': go.Layout(
            title='Comparison of indicators',
            xaxis={
                'title': xaxis_column_name + '\n' + ', million euro',
                'titlefont': dict(size=16),
                'type':'linear' if axis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name+ '\n' + ', million euro',
                'titlefont': dict(size=16),
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            margin={'l': 100, 'b': 40, 't': 40, 'r': 100},
            hovermode='closest'
        )
    }

#SECOND GRAPH

@app.callback(
    dash.dependencies.Output('indicator_graphic_country', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis_column_2', 'value'),
     dash.dependencies.Input('axis_type_2', 'value'),
     dash.dependencies.Input('unit_2', 'value')])
    
def update_graph_2(country, yaxis_column_2,
                 axis_type_2,unit_2):
    dff=df[df['GEO']== country]
    dfff= dff[dff['UNIT']==unit_2]
    return {
        'data': [go.Scatter(
            x=dfff['TIME'].unique(),
            y=dfff[dfff['NA_ITEM'] == yaxis_column_2]['Value'],
            text=dfff[dfff['NA_ITEM'] == yaxis_column_2]['GEO'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        
        'layout': go.Layout(
            title= yaxis_column_2 + ' / ' + country,
            xaxis={'title': 'Years',
                   'titlefont': dict(
                       size=16)
                  },
            yaxis={
                'title': yaxis_column_2 +'\n' + ', million euro',
                'titlefont': dict(size=16),
                'type': 'linear' if axis_type_2 == 'Linear' else 'log'},
            margin={'l': 100, 'b': 60, 't': 60, 'r': 100},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()


