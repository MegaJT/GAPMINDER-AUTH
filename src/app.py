import pandas as pd
import bcrypt
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
from dash import html, dcc
from dash.dependencies import Input, Output
from flask import Flask, request, Response,session
import bcrypt



# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
server = Flask(__name__)
app = Dash(__name__, server=server,external_stylesheets=[dbc.themes.COSMO])
server=app.server


users_df = pd.read_excel('users.xlsx')
def check_auth(username, password):
    """Check if a username / password combination is valid."""
    user_record = users_df[users_df['username'] == username]
    if not user_record.empty:
        stored_password = user_record.iloc[0]['password']
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

@server.before_request
def before_request():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()












shadowstyle='0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
logo=html.Img(src='../assets/logo.jpeg',width=100,height=100,style={'box-shadow': shadowstyle})
Title=html.Div("GAPMINDER",style={'text-align':'center','background':'#f0f0f0','font-size': '65px','box-shadow': shadowstyle})


#'background-color':'#deb887',
CardHeaderStyle={'border-color':'#4CAF50',
        'border-width':'100px',
        'border-radius': '10px 10px 0px 0px',
        'box-shadow':shadowstyle,
        #'background-image': 'linear-gradient(to left, rgba(255,0,0,0), rgba(255,0,0,1))',
        'background':'#bfff00',
        'font-size': '25px',
        'text-align': 'center',
        'color': 'black',
        'margin-top': '30px',
        'margin-left': '10px',
        'margin-right': '10px',
        'margin-bottom': '0px',
        'vertical-align':'middle',
        'align-items':'center',
        }

CardFooterStyle={'border-color':'#4CAF50',
        'border-width':'100px',
        'border-radius': '10px 10px 10px 10px',
        'box-shadow':shadowstyle,
        'background':'#20B2AA',
        'font-size': '25px',
        'text-align': 'center',
        'color': 'black',
        'margin-top': '0px',
        'margin-left': '10px',
        'margin-right': '10px',
        'margin-bottom': '10px',
        'vertical-align':'middle',
        'align-items':'center',
        
                
        }


cardstyle={'height': '200px',
  'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
  'text-align': 'center',
  'background-color': '#4CAF50',
  'color': 'white',
  'padding': '10px',
  'margin-top': '0px',
  'margin-left': '10px',
  'margin-right': '10px',
  'margin-bottom': '0px',
  'font-size': '100px',
  #'text-shadow': '2px 2px 4px #000000',
  'border-radius': '0px 0px 10px 10px'}


# Incorporate data into App
df = px.data.gapminder()
continent_life_expectancy = df.groupby('continent')['lifeExp'].mean()

# Filter data for a specific country
country_data = df[df['country'] == 'United States']

# Get unique continent and country values

unique_countries = df['country'].unique()

unique_continents = df['continent'].unique()



# Dropdown for continents
data=unique_continents
continent_dropdown = dcc.Dropdown(
    id='continent-dropdown',
    #options=[{'label': continent, 'value': continent} for continent in unique_continents],
    #value=unique_continents[0],  # Set default value to the first continent
    placeholder="Select a continent"
)

# Dropdown for countries
country_dropdown = dcc.Dropdown(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in unique_countries],
    value=unique_countries[0],  # Set default value to the first country
    placeholder="Select a country"
)

# Generate Plotly Express chart
#fig = px.line(country_data, x='year', y='lifeExp', title='Life Expectancy Over Time for United States')
#fig = px.scatter(country_data, x='year', y='lifeExp', title='Life Expectancy Over Time for United States')
fig = px.bar(country_data,x='year', y='lifeExp', text='lifeExp', title='Life Expectancy')
#fig = px.box(country_data, x='year', y='lifeExp', title='Life Expectancy Over Time for United States')
#fig = px.choropleth(country_data, locations='country', locationmode='country names', color='lifeExp', hover_name='country', title='Life Expectancy Across Countries')

# Identify the latest year in the DataFrame
latest_year = df['year'].max()

# Filter data for the latest year
latest_year_data = df[df['year'] == latest_year]

# Get unique years from the DataFrame
years = df['year'].unique()







# Convert the Plotly Express chart to a Div element
bar_chart = dcc.Graph(id='bar_chart',figure=fig)

# Define layout components
Bub_Chart_and_slider = html.Div([
    dcc.Graph(id='bubble-chart', figure=[]),
    html.Br(),
    dcc.Slider(
        id='year-slider',
        min=years.min(),
        max=years.max(),
        value=years.min(),
        marks={str(year): str(year) for year in years},
        step=None
    )
])


# Build the layout to define what will be displayed on the page
app.layout =html.Div([
dbc.Row([
        dbc.Col([logo],width=2),
        dbc.Col([Title],width=8),
        dbc.Col([],width=2,id='output-username')
    ]),
dbc.Row([html.Hr()]),       
dcc.Tabs([
dcc.Tab(label='Life Expectancy', children=[
dbc.Container([
dbc.Row([
        dbc.Col([dbc.Row([continent_life_expectancy.index[0]],justify='center',style=CardHeaderStyle),dbc.Row([round(continent_life_expectancy.iloc[0])],justify='center',style=cardstyle),dbc.Row(['99'],justify='center',style=CardFooterStyle)]),
        dbc.Col([dbc.Row([continent_life_expectancy.index[1]],justify='center',style=CardHeaderStyle),dbc.Row([round(continent_life_expectancy.iloc[1])],justify='center',style=cardstyle),dbc.Row(['99'],justify='center',style=CardFooterStyle)]),
        dbc.Col([dbc.Row([continent_life_expectancy.index[2]],justify='center',style=CardHeaderStyle),dbc.Row([round(continent_life_expectancy.iloc[2])],justify='center',style=cardstyle),dbc.Row(['99'],justify='center',style=CardFooterStyle)]),
        dbc.Col([dbc.Row([continent_life_expectancy.index[3]],justify='center',style=CardHeaderStyle),dbc.Row([round(continent_life_expectancy.iloc[3])],justify='center',style=cardstyle),dbc.Row(['99'],justify='center',style=CardFooterStyle)]),
        ]),
dbc.Row([html.Hr()]),      
dbc.Row([ dbc.Col(continent_dropdown), dbc.Col(country_dropdown) ]),      
dbc.Row([bar_chart]),                 

],fluid=True),

  ]),
        dcc.Tab(label='GDP per Capita', children=[
            dbc.Container([Bub_Chart_and_slider]),])    ])
    ])


# Callback to filter content based on username
@app.callback(
    Output('continent-dropdown', 'options'),
    [Input('output-username', 'children')]
)
def filter_dropdown_content(_):
    auth = request.authorization
    if not auth:
        return []

    username = auth.username
    if username == 'user1':
        filtered_items = data[:2]
    elif username == 'user2':
        filtered_items = data[:3]
    elif username == 'user3':
        filtered_items = data[:4]
    else:
        filtered_items = []

    return [{'label': item, 'value': item} for item in filtered_items]


# Callback to update country dropdown options based on selected continent
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('continent-dropdown', 'value')]
)
def update_country_dropdown(selected_continent):
    if selected_continent is None:
        return []
    else:
        # Get unique countries for the selected continent
        countries_for_continent = df[df['continent'] == selected_continent]['country'].unique()
        options = [{'label': country, 'value': country} for country in countries_for_continent]
        return options

# Callback to update plot and title based on selected country
@app.callback(
    [Output('bar_chart', 'figure') ],
    [Input('country-dropdown', 'value')]
)
def update_plot(selected_country):
    # Filter data for the selected country
    country_data = df[df['country'] == selected_country]

     # Round life expectancy values to nearest two-digit decimal
    country_data.loc[:,'lifeExp'] = country_data['lifeExp'].round(2)
    #print(country_data)
    
    # Update plot
    fig = px.bar(country_data, x='year', y='lifeExp', text='lifeExp')

    # Set the tickvals and ticktext for the x-axis to display year values for each bar
    fig.update_layout(xaxis=dict(
        tickvals=country_data['year'],
        ticktext=country_data['year']
    ))
    
    # Update title
    if selected_country:
        fig.update_layout(title=f'Life Expectancy Over Time for {selected_country}')
    else:
        fig.update_layout(title='Life Expectancy dummy')

    return [fig]


# Define callback to update the scatter plot based on the selected year
@app.callback(
    Output('bubble-chart', 'figure'),
    [Input('year-slider', 'value')]
)
def update_plot(selected_year):
    # Filter data for the selected year
    filtered_data = df[df['year'] == selected_year].copy()
    
    # Create the bubble chart
    bub_fig = px.scatter(filtered_data, y='pop', x='gdpPercap',
                 size='pop', color='country',
                 hover_name='country', log_x=False, log_y=True,
                 labels={'gdpPercap': 'GDP per Capita', 'pop': 'Population'},
                 title='GDP per Capita vs Population',
                 size_max=75) 

# Update layout
    bub_fig.update_layout(xaxis_title='GDP per Capita (log scale)',
                  yaxis_title='Population (log scale)',
                  showlegend=False)

    return bub_fig



# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
    
    