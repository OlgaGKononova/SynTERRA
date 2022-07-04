from imasyndata_web.plotly_config import BG_COLOR_PLOT

SYN_GRAPH_STYLESHEET = {
    "nodes": {"shape": "circle",
              "width": 45,
              "height": 45,
              "background-color": BG_COLOR_PLOT,
              "background-fit": "cover",
              "background-image": "data(url)"
    },
    "edges": {"curve-style": "unbundled-bezier",
              "target-arrow-color": "grey",
              "target-arrow-shape": "vee",
              "line-color": "grey",
              "arrow-scale": 1.0,
              "source-distance-from-node": 0.1,
              "target-distance-from-node": 0.1,
              #"source-endpoint": "180deg",
              #"target-endpoint": "0deg",
    },
    "edge_width_scale": 2
}