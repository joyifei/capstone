# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df['Status'] = spacex_df['class'].apply( lambda x: 'Success' if x == 1 else 'Failure')
spacex_df['count'] = 1.0
sites = spacex_df["Launch Site"].unique()
dropdown_options = []
for site in sites:
    dropdown_options.append( {'label':site, 'value':site},)
dropdown_options.append( {'label':"All Sites",'value':'ALL'},)
# Create a dash application
print( dropdown_options )
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                dcc.Dropdown(id='site-dropdown', 
                                             options=dropdown_options,
                                             value = 'ALL', 
                                             placeholder="place holder here",
                                             searchable = True ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload, max = max_payload, step = 1000, value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output( component_id='success-pie-chart', component_property='figure'),
                Input( component_id = 'site-dropdown', component_property='value'))
def get_pie_chart( entered_site ):
    print( spacex_df.head(5) )
    if entered_site =='ALL':
        fig = px.pie( spacex_df, values='class', names = 'Launch Site', title = entered_site)
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie( filtered_df, values='count', names = 'Status', title = entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")] )

def get_scatter_chart( entered_site, slider_range ):
    low, high = slider_range
    sliderrange_df = spacex_df[spacex_df['Payload Mass (kg)']>=low]
    sliderrange_df = sliderrange_df[sliderrange_df['Payload Mass (kg)']<=high]

    if entered_site == 'ALL':
        fig = px.scatter( sliderrange_df, x='Payload Mass (kg)', y='class', color="Booster Version Category", hover_data=["Booster Version"], title = 'correlation between payload mass and success' )
        return fig
    else:
        filtered_df = sliderrange_df[sliderrange_df['Launch Site']==entered_site]
        fig = px.scatter( filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category", hover_data=["Booster Version"], title = 'correlation between payload mass and success ' + entered_site )
        return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server()
