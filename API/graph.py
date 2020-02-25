import plotly.graph_objects as go 
import pandas as pd 

def candle(data,*args,buy=None,sell=None):
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(x=data['datetime'],
                        open=data['open'],
                        high=data['high'],
                        low=data['low'],
                        close=data['close'],
                        name='Candlestick'))
    i = 0
    for arg in args:
        i+=1
        fig.add_trace(
            go.Scatter(
                x=data['datetime'],
                y=arg,
                name=i,
                line=dict(
                    color='#50e680',
                    width=1
                )
            )
        )

    if buy is not None:
        for i in enumerate(buy):
            fig.add_annotation(
                x=i[1],
                y=data.loc[i[0],'open']-1,
                xref='x',
                yref='y',
                ax=0,
                ay=-10,
                text=None,
                showarrow=True,
                arrowhead=1,
                arrowsize=4,
                arrowwidth=1,
                arrowcolor='#086309',
                opacity=1
            )
    if sell is not None:
        for i in enumerate(sell):
            fig.add_annotation(
                x=i[1],
                y=data.loc[i[0],'open'],
                xref='x',
                yref='y',
                ax=0,
                ay=10,
                text=None,
                showarrow=True,
                arrowhead=1,
                arrowsize=4,
                arrowwidth=1,
                arrowcolor='#990606',
                opacity=1
            )

    fig.update_layout(
        template='plotly_dark',
        font=dict(
            family='Arial',
            size=11
        ),
        # plot_bgcolor='rgb(0,0,0)'
    )

    fig.show()