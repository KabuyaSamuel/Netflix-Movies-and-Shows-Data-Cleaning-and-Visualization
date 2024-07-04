import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Load the dataset
netflix_movies = pd.read_csv("netflix_movies.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Netflix Dashboard"),
    
    # Dropdown for selecting genre
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': genre, 'value': genre} for genre in netflix_movies['listed_in'].unique()],
        multi=True,
        placeholder="Select Genre"
    ),
    
    # Dropdown for selecting release year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in netflix_movies['release_year'].unique()],
        multi=True,
        placeholder="Select Release Year"
    ),
    
        # Dropdown for selecting country
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': country, 'value': country}
            for country in netflix_movies['country'].unique() if pd.notna(country)
        ],
        multi=True,
        placeholder="Select Country"
    ),
        # Display the filtered data
        html.Div(id='output-div')
    ])

# Define callback to update the output based on user input
@app.callback(
    Output('output-div', 'children'),
    [Input('genre-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_output(selected_genres, selected_years, selected_countries):
    filtered_data = netflix_movies

    # Filter by selected genre(s)
    if selected_genres:
        filtered_data = filtered_data[filtered_data['listed_in'].str.contains('|'.join(selected_genres))]

    # Filter by selected release year(s)
    if selected_years:
        filtered_data = filtered_data[filtered_data['release_year'].isin(selected_years)]

    # Filter by selected country(ies)
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    # Display the filtered data in a DataTable
    table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in filtered_data.columns])] +

        # Body
        [html.Tr([html.Td(filtered_data.iloc[i][col]) for col in filtered_data.columns]) for i in range(min(len(filtered_data), 10))]
    )

    return table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
