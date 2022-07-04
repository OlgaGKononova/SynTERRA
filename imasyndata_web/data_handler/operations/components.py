import pandas as pd
from copy import deepcopy

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto

from imasyndata_web.utils import get_bins_number
from imasyndata_web.data_handler.precursors.components import precursors_stats_figure
from imasyndata_web.plotly_config import \
    TEMPERATURE_COLORS, TIME_COLORS, ENVIRONMENT_COLORS, PLOT_AXIS_STYLE, FONT, BG_COLOR, BG_COLOR_PLOT, GRID_COLOR
from imasyndata_web.data_handler.operations.constants import \
    DEFAULT_ATTRIBUTES_LBL, DEFAULT_PRECURSORS_LBL, ATTRIBUTES_PLOT_TITLE

cyto.load_extra_layouts() # needed to export svg

def synthesis_graph(elements, style, max_value, marks):
    return [html.Label("Synthesis Graph:",
                       style={"font-weight": "700"}),
            html.P("\n\n\n"),
            dcc.Slider(id="threshold_slider",
                       min=0, max=max_value, step=1, value=0, marks=marks),
            html.P("\n\n"),
            cyto.Cytoscape(id="cytoscape-pane",
                           layout={"name": "preset", "fit": True, "padding": "5px"},
                           style={"height": "700px",
                                  "border": "1px solid #F19F4D",
                                  "background-color": BG_COLOR_PLOT},
                           elements=elements,
                           stylesheet=style),
            html.P("\n\n"),
            html.Div([html.Button("Export graph",
                                  className="button-primary",
                                  id="export_graph_btn")])
            ]


def plot_operation_attributes(attributes_data, graph_id):
    """

    :param attributes_data: dict(temperature: list, time: list, environment: list)
    :param graph_id:
    :return:
    """
    num_col = len(attributes_data)
    attributes_plot = make_subplots(rows=1, cols=num_col, horizontal_spacing=0.1,
                                    subplot_titles=[ATTRIBUTES_PLOT_TITLE[k] for k in attributes_data.keys()])

    temperature = [t for t in attributes_data["temperature"] if 0 < t < 3000]
    nbins = get_bins_number(temperature)
    temp_hist = go.Histogram(x=temperature,
                             nbinsx=nbins, text=nbins,
                             marker=dict(color=TEMPERATURE_COLORS["bars_marker"],
                                         line=dict(color=TEMPERATURE_COLORS["bars_line"],
                                                   width=2)))

    time = [t for t in attributes_data["time"] if 0 < t < 1000]
    nbins = get_bins_number(time)
    time_hist = go.Histogram(x=time,
                             nbinsx=nbins, text=nbins,
                             marker=dict(color=TIME_COLORS["bars_marker"],
                                         line=dict(color=TIME_COLORS["bars_line"],
                                                   width=2)))

    env_hist = go.Histogram(x=attributes_data["environment"],
                            marker=dict(color=ENVIRONMENT_COLORS["bars_marker"],
                                        line=dict(color=ENVIRONMENT_COLORS["bars_line"],
                                                  width=2)))
    attributes_plot.append_trace(temp_hist, row=1, col=1)
    attributes_plot.append_trace(time_hist, row=1, col=2)
    attributes_plot.append_trace(env_hist, row=1, col=3)

    for num in range(num_col):
        xaxis_style = deepcopy(PLOT_AXIS_STYLE["xaxis"])
        yaxis_style = deepcopy(PLOT_AXIS_STYLE["yaxis"])
        xaxis_style["title_text"] = ""
        xaxis_style["showgrid"] = False
        del yaxis_style["dtick"]
        yaxis_style["title_text"] = "Amount"
        yaxis_style["title_standoff"] = 10
        yaxis_style["showgrid"] = True
        yaxis_style["gridcolor"] = GRID_COLOR
        axis_style = {"xaxis" + str(num + 1): xaxis_style,
                      "yaxis" + str(num + 1): yaxis_style}
        attributes_plot.update_layout(axis_style)

    attributes_plot.update_annotations(font=FONT["plot_title"])
    attributes_plot.update_layout(autosize=True,
                                  height=300,
                                  showlegend=False,
                                  paper_bgcolor=BG_COLOR,
                                  plot_bgcolor=BG_COLOR_PLOT,
                                  margin=dict(pad=0, l=0, r=0, t=25))
    return dcc.Graph(id=graph_id, figure=attributes_plot)


def plot_operation_precursors(all_precursors, graph_id):
    precursors_plot = precursors_stats_figure(all_precursors)
    precursors_plot["layout"].update(autosize=True,
                                     height=400,
                                     plot_bgcolor=BG_COLOR_PLOT,
                                     paper_bgcolor=BG_COLOR,
                                     margin=dict(t=5),
                                     yaxis=PLOT_AXIS_STYLE["yaxis"]
                                     )
    return dcc.Graph(id=graph_id, figure=precursors_plot)


def synthesis_attributes():
    return [html.Details([html.Summary(DEFAULT_ATTRIBUTES_LBL,
                                       id="operations-attributes_sum",
                                       style={"font-weight": "700", "marginBottom": "10px"}),
                          html.Div("Click a graph node to display attributes...",
                                   id="operations-attributes_plot",
                                   style={"align": "center", "margin": "0px", "padding": "0px"})],
                         open="open",
                         style={"padding": "10px", "margin-top": "40px"}),
            html.Details([html.Summary(DEFAULT_PRECURSORS_LBL,
                                       id="precursors-attributes_sum",
                                       style={"font-weight": "700", "marginBottom": "10px"}),
                          html.Div("Click a graph edge to display precursors...",
                                   id="precursors-attributes_plot",
                                   style={"align": "center", "margin": "0px", "padding": "0px"})],
                         open="open",
                         style={"padding": "10px"})]


def serve_layout(graph_elements, graph_style, max_value, marks):

    return [html.Div(synthesis_graph(graph_elements, graph_style, max_value, marks),
                     className="five columns",
                     style={"marginTop": "20px"}),
            html.Div(synthesis_attributes(), className="seven columns")]
