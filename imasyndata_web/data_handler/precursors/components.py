from copy import deepcopy
import plotly
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html

from imasyndata_web.plotly_config import PRECURSOR_COLORS, PLOT_TITLE_STYLE, PLOT_AXIS_STYLE, BG_COLOR, BG_COLOR_PLOT


def precursors_stats_figure(precursors_stat, graph_title=""):

    precursors_bars = go.Bar(x=[count for m, count in precursors_stat],
                             y=[m for m, count in precursors_stat],
                             orientation="h",
                             width=[0.8]*len(precursors_stat),
                             marker=dict(color=PRECURSOR_COLORS["bars_marker"],
                                         line=dict(color=PRECURSOR_COLORS["bars_line"],
                                                   width=2)))

    max_len = max([len(m) for m, count in precursors_stat]) if precursors_stat else 0

    layout = go.Layout(title=graph_title,
                       height=500 if len(precursors_stat) < 30 else len(precursors_stat) * 20,
                       margin=dict(l=max_len * 9.0, r=5, t=70, b=60))

    layout.update(PLOT_TITLE_STYLE)
    xaxis_layout = deepcopy(PLOT_AXIS_STYLE["xaxis"])
    xaxis_layout.update(dict(title_text="Amount"))
    layout.update(dict(xaxis=xaxis_layout))
    layout.update(dict(paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT))
    figure = {"data": [precursors_bars],
              "layout": layout}

    return figure


def precursors_stats_plot(precursors_stat, graph_id, graph_title=""):
    return dcc.Graph(figure=precursors_stats_figure(precursors_stat, graph_title),
                     id=graph_id)
