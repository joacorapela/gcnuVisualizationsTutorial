
import sys
import numpy as np
import plotly.graph_objs as go

def main(argv):
    latentsFilename = "results/latents.npy"
    figFilenamePattern = "figures/latent{:d}.{:s}"
    latents = np.load(latentsFilename, allow_pickle=True)
    nLatents = latents.shape[0]
    for k in range(nLatents):
        figDic = {"data": {"type": "scatter", 
                           "x": np.arange(latents.shape[1]),
                           "y": latents[k,:]},
                  "layout": {"title": "Latent {:d}".format(k+1),
                             "yaxis": {"range": [0, 3]},
                             "xaxis_title": "Sample",
                             "yaxis_title": "Latent",
                             },
                 }
        fig = go.Figure(figDic)
        fig.write_image(figFilenamePattern.format(k+1, "png"))
        fig.write_html(figFilenamePattern.format(k+1, "html"))

if __name__=="__main__":
    main(sys.argv)
