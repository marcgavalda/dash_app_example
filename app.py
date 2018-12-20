import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('nama_10_gdp_1_Data.csv')

#DATA CLEANING
df = df.drop(df[df.GEO.isin(["European Union (current composition)",
                    "European Union (without United Kingdom)",
                    "European Union (15 countries)",
                    "Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)",
                    "Euro area (12 countries)",
                    "Euro area (19 countries)"])].index)

df= df.drop(columns=['Flag and Footnotes'])
df= df.drop(df[df.Value.isin([':'])].index) 

available_indicators = df['NA_ITEM'].unique()
available_country = df['GEO'].unique()
available_unit=df['UNIT'].unique()

#FIRST PART LAYOUT
app.layout = html.Div([
    html.H1('Cloud Computing Final Assigment',style={'textAlign': 'center'}),
    html.H2('Relationship between indicators, by country',style={'textAlign': 'left', 'size': 15,'color': 'black'}),
    html.Div([
        html.Div([
            html.Label('Select Indicator for X axis'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            html.Div(style={'height': 10, 'display': 'inline-block'}),
            html.Label('Select Unit'),
            dcc.Dropdown(
                id='unit',
                options=[{'label': i, 'value': i} for i in available_unit],
                value="Chain linked volumes, index 2010=100")
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
    
    dcc.Graph(
            id='indicator-graphic',
            hoverData={'points': [{'customdata': 'Belgium'}]}
        ),
    
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
    html.H3('Evolution of Indicator, by country', style={'textAlign': 'left', 'size': 15,'color': 'black'}),
     html.Div([
             html.H2(children=''),
        html.Div([
            html.Label('Select Indicator'),
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],style={'width': '40%', 'display': 'inline-block','margin': 20}),
        html.Div([
            html.Label('Select country'),
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_country],
                value='Belgium')],
            style={'width': '40%', 'float':'right', 'display': 'inline-block','margin': 20}),
     html.Div([
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in available_unit],
                value='Chain linked volumes, index 2010=100',
                labelStyle={'display': 'inline-block','margin':10}
            )],
            style={'width': '88%', 'display': 'inline-block','margin': 30})
    ]),

    dcc.Graph(id='country-indicator-graphic')
])
    
# FIRST INDICATOR 
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('axis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('unit', 'value')])
    
def update_graph(xaxis_column_name, yaxis_column_name, 
                 axis_type,year_value,unit):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit)]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name) & (dff['GEO']== i)]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name) & (dff['GEO']== i)]['Value'],
            text=dff[(dff['NA_ITEM'] == yaxis_column_name) & (dff['GEO']== i)]['GEO'],
            customdata=dff[(dff['NA_ITEM'] == yaxis_column_name)&(dff['GEO']== i)]['GEO'],
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

#SECOND INDICATOR
@app.callback(
    dash.dependencies.Output('country-indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'), 
     dash.dependencies.Input('unit', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, unit):
        dff = df[(df['GEO'] == yaxis_column_name) & (df['UNIT'] == unit)]
        return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='lines',
            line=dict(
                color= ('rgb(170,24,175)')),
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 60, 'b': 60, 't': 60, 'r': 60},
            title= 'Evolution of indicator from 2008 to 2017',
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()