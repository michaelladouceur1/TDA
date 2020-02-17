import plotly.graph_objects as go 
import pandas as pd 

def candle(data,*args):
    # fig = go.Figure(data=[go.Candlestick(x=data['datetime'],
    #                 open=data['open'],
    #                 high=data['high'],
    #                 low=data['low'],
    #                 close=data['close'])])
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(x=data['datetime'],
                        open=data['open'],
                        high=data['high'],
                        low=data['low'],
                        close=data['close'],
                        name='Candlestick'))
    
    for arg in args:
        fig.add_trace(
            go.Scatter(
                x=data['datetime'],
                y=data[arg],
                name=arg
            )
        )

    fig.update_layout(
        template='plotly',
        font=dict(
            family='Arial',
            size=11
        )
    )

    fig.show()