import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

app = dash.Dash(__name__)
server = app.server

people = ['Chris', 'Sam', 'Ella', 'Lee', 'Will', 'James', 'Jahnavi', 'Tom', 'Mike S', 'Mike G', 'Jamie', 'Shaun', 'Krupen', "Kam"]

df = pd.DataFrame(columns=['Name', 'Date', 'Mood'])

app.layout = html.Div([
    dcc.Dropdown(
        id='name-dropdown',
        options=[{'label': name, 'value': name} for name in people],
        placeholder='Select your name'
    ),
    dcc.Dropdown(
        id='mood-dropdown',
        options=[{'label': i, 'value': i} for i in range(1, 11)],
        placeholder='Submit your mood score'
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output'),
    dcc.Graph(id='mood-graph')
])

@app.callback(
    Output('output', 'children'),
    Input('submit-button', 'n_clicks'),
    [dash.dependencies.State('name-dropdown', 'value'),
     dash.dependencies.State('mood-dropdown', 'value')]
)
def save_mood_data(n_clicks, name, mood_score):
    global df
    if n_clicks > 0 and name is not None and mood_score is not None:
        current_date = datetime.now().date()
        df = pd.concat([df, pd.DataFrame({'Name': name, 'Date': current_date, 'Mood': mood_score}, index=[len(df)])])
        df = df.drop_duplicates(keep="last")
        df.to_csv('moods.csv', index=False)
        return f'Mood data submitted successfully for {name} on {current_date}'
    return ''


@app.callback(
    Output('mood-graph', 'figure'),
    Input('submit-button', 'n_clicks')
)
def update_graph(n_clicks):
    if not df.empty:
        fig = px.line(df, x='Date', y='Mood', color='Name', markers=True, title='Mood Over Time')
        return fig
    return px.line(title='Mood Over Time')


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8055)
