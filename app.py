import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime as date
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)
# server = app.server

def get_stock_price_fig(df):
    fig = px.line(df, x="Date", y=["Close", "Open"], title="Closing and Opening Price vs Date", markers=True)
    fig.update_layout(title_x=0.5)
    return fig

def get_more(df):
    df['EWA_20'] = df['Close'].ewn(span=20, adjust=False).mean()
    fig = px.scatter(df, x= "Date", y="EWA_20", title="Exponential Moving Average vs Date")
    fig.update_traces(mode="Line+Marker")
    return fig

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
        

@app.callback([
    Output('description', 'children'),
    Output('logo', 'src'),
    Output('name', 'children'),
    Output('submit-val', 'n_clicks'),
    Output('submit-ind', 'n_clicks'),
    Output('submit-forc', 'n_clicks'),
    Input('submit-name', 'n_clicks'),
    State('input', 'value')])

def update_data(n,val):
    if n == None:
        return "Please enter a legitimate stock code to get details!"
    else:
        if val == None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            df[['logo_url', 'short_name', 'longBusinessSummary']]
            return df['longBusinessSummary'].values[0], df['logo_url'].values[0], df['short_name'].values[0], None, None, None
        

@app.callback([
    Output('graphs_content', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    State('input', 'value')])

def update_graph(n,start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)
    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]

@app.callback([
    Output('main-content', 'children'),
    Input('subit-ind', 'n_clicks'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    State('input', 'value')
])

def indicators(n,start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]
    
    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]

@app.callback([
    Output('forecast-content', 'children'),
    Input('subit-forc', 'n_clicks'),
    State('Forecast_Input', 'value'),
    State('input', 'value')
])

# def forecast(n,n_days, val):
#     if n == None:
#         return [""]
#     if val == None:
#         raise PreventUpdate
#     x=int(n_days)
#     fig = predict(val, x+1)
#     return [dcc.Graph(figure=fig)]

if __name__ == "__main__":
  app.run_server(debug=True)