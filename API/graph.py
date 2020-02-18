import plotly.graph_objects as go 
import pandas as pd 

def candle(data,*args,bsh=False):
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
                name=arg,
                line=dict(
                    color='#50e680',
                    width=1
                )
            )
        )

    if bsh == True:
        for i in enumerate(data['bsh']):
            if i[1] == 'buy':
                fig.add_annotation(
                    x=data.loc[i[0],'datetime'],
                    y=data.loc[i[0],'open']+4,
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
            elif i[1] == 'sell':
                fig.add_annotation(
                    x=data.loc[i[0],'datetime'],
                    y=data.loc[i[0],'open']-4,
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