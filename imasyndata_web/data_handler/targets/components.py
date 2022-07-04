import plotly
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html

from imasyndata_web.plotly_config import TARGET_COLORS, PLOT_TITLE_STYLE, PLOT_AXIS_STYLE, FONT, BG_COLOR, BG_COLOR_PLOT

from pprint import pprint
from copy import deepcopy


def targets_stats_plot(targets_stat, graph_id, graph_title=""):

    target_bars = go.Bar(x=[count for m, count in targets_stat],
                         y=[m for m, count in targets_stat],
                         orientation="h",
                         width=[0.8 for _ in targets_stat],
                         marker=dict(color=TARGET_COLORS["bars_marker"],
                                     line=dict(color=TARGET_COLORS["bars_line"],
                                               width=2)))

    max_len = max([len(m) for m, count in targets_stat]) if targets_stat else 0

    layout = go.Layout(title=graph_title,
                       height=500 if len(targets_stat) < 30 else len(targets_stat) * 20,
                       margin=dict(l=max_len * 9.0, r=5, t=70, b=60))

    layout.update(PLOT_TITLE_STYLE)
    axis_style = deepcopy(PLOT_AXIS_STYLE)
    axis_style["xaxis"].update(dict(title_text="Amount"))
    layout.update(axis_style)
    layout.update(dict(paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT))
    figure = {"data": [target_bars],
              "layout": layout}

    return dcc.Graph(figure=figure,
                     id=graph_id)
