import dash
from dash import dcc
from dash import html
from datetime import datetime as date
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
html.Div(
          [
            html.P("Hi,welcome to Stock Dash App", className="start"),
            html.Div([
                dcc.Input(id='input', type='text', style={'align':'center'}),
                html.Button('submit',id='submit-name', n_clicks=0),
            ]),
            html.Div([
             'Select a date range: ',
                        dcc.DatePickerRange(
                          id='my-date-picker-range',
                          min_date_allowed=date (2003,1,1),
                          max_date_allowed=date.now(),
                          initial_visible_month=date.now(),
                          end_date=date.now().date(),
                          style = {'font-size':'18px','display':'initial-block','align':'center','border-radius':'2px','border':'1px solid #ccc','color':'#333'}
                        ),
              html.Div(id='output-container-date-picker-range',children='Date has been selected')        
            ]),
            html.Div([
              html.Button('Stock price',id='submit-val',n_clicks=0,style={'float':'left','padding':'15px 32px','background-color':'red','display':'inline'}),
              html.Div(id='container-button-basic'),
              html.Button('Indicator',id='submit-ind', n_clicks=0),
              html.Div([dcc.Input(id='Forcast_Input',type='text',)]),
              html.Button('No of days to forcast',id='submit-force', n_clicks=0),
              html.Div(id='forcast')
            ]),
          ],className="nav"
        ),
html.Div([
            html.Div([
              html.Img(id='logo'),
              html.H1(id='name')
                ],
              className="header"),
              html.Div( 
                id="description", className="decription_ticker"),
              html.Div([], 
               id="graphs-content"),
              html.Div([],
               id="main-content"),
              html.Div([],
               id="forecast-content")
            ],
          className="content"),
])
if __name__ == '__main__':
    app.run_server(debug=True)
        

