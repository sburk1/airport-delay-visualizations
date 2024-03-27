import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read data
ports_with_location = pd.read_csv("ports_with_location_copy.csv")

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define layout of the app
app.layout = html.Div([
    dcc.Graph(id='map-plot'),
    html.Label("Select which type of delay to color the graph by:"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Average Departure Delay', 'value': 'ave_departure_delay'},
            {'label': 'Average Arrival Delay', 'value': 'ave_arrival_delay'}
        ],
        value='ave_departure_delay',  # Default value
        clearable=False
    )
])

# Define callback to update the plot based on dropdown selection
@app.callback(
    Output('map-plot', 'figure'),
    [Input('dropdown', 'value')]
)
def update_plot(selected_metric):
    fig = px.scatter_geo(
        data_frame=ports_with_location, 
        lat="latitude_deg", 
        lon="longitude_deg",
        hover_name="name",
        projection="albers usa",
        hover_data=["ave_departure_delay", "ave_arrival_delay"],
        color=selected_metric
    )

    # Country and state boundaries
    fig.update_geos(
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Blue",
    )

    # Custom text in boxes
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>' +
                                     'Average Departure Delay: %{customdata[0]:.2f} min<br>' +
                                     'Average Arrival Delay: %{customdata[1]:.2f} min<br>' +
                                     '<extra></extra>')

    # Update color bar title dynamically based on the selected dropdown value
    fig.update_layout(title_text="Average Delays at American Airports",
                      coloraxis_colorbar_title=selected_metric.replace("_", " ").replace("ave", "Average").title() + " (mins)")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)