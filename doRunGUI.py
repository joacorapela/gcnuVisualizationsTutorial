
import pdb
import sys
import os
import time
import multiprocessing as mp
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.exceptions
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

def serve_layout():
    aDiv = html.Div(children=[
        html.H1(children="Tea Talk Dash/Plotly Tutorial"),
        html.Hr(),
        html.Button("Estimate", id="doEstimate", n_clicks=0),
        html.Div(id="pid", children="pid: None", hidden=False),
        html.Label("Latent to Plot"),
        dcc.Dropdown(
            id="latentToPlotComponent",
            options=[
                {"label": "1", "value": 1},
                {"label": "2", "value": 2},
                {"label": "3", "value": 3},
            ],
            value=1,
            style={"width": "30%"},
        ),
        dcc.Graph(id="latentGraph"),
        dcc.Interval(
            id="updateGraphInterval",
            interval=1*1000, # in milliseconds
            n_intervals=0,
            disabled=False,
        ),
    ])
    return aDiv

def runEstimation():
    nLatents = 3
    nSamples = 100
    nIter = 30
    sleepTime = 1
    latentsFilename = "results/latents.npy"
    for i in range(nIter):
        latents = np.empty(shape=(nLatents, nSamples))
        latents[0,:] = np.random.uniform(size=(1, nSamples), low=0, high=1)
        latents[1,:] = np.random.uniform(size=(1, nSamples), low=1, high=2)
        latents[2,:] = np.random.uniform(size=(1, nSamples), low=2, high=3)
        np.save(file=latentsFilename, arr=latents)
        time.sleep(sleepTime)

def main(argv):

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = serve_layout

    @app.callback(Output("pid", "children"),
                  [Input("doEstimate", "n_clicks")])
    def runEstimationCallback(doEstimateNClicks):
        if doEstimateNClicks>0:
            p = mp.Process(target=runEstimation)
            p.start()
            pidChildren = "pid: {:d}".format(p.pid)
            return pidChildren
        raise dash.exceptions.PreventUpdate

    @app.callback(Output("latentGraph", "figure"),
                  [Input("updateGraphInterval", "n_intervals")],
                  [State("latentToPlotComponent", "value"),
                   State("doEstimate", "n_clicks")],
                  )
    def updateLatentsGraph(nIntervals, latentToPlot, doEstimateNClicks):
            latentsFilename = "results/latents.npy"
            if doEstimateNClicks>0 and os.path.exists(latentsFilename):
                latents = np.load(latentsFilename, allow_pickle=True)
                figDic = {"data": {"type": "scatter", 
                                   "x": np.arange(latents.shape[1]),
                                   "y": latents[latentToPlot-1,:]},
                          "layout": {"title": "Latent {:d}".format(latentToPlot),
                                     "yaxis": {"range": [0, 3]},
                                     "xaxis_title": "Sample",
                                     "yaxis_title": "Latent",
                                    },
                         }
                fig = go.Figure(figDic)
                return fig
            else:
                raise dash.exceptions.PreventUpdate

    app.run_server(debug=True)

if __name__ == "__main__":
    main(sys.argv)

