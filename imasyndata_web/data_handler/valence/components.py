import numpy as np
from copy import deepcopy

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html

from imasyndata_web.constants import METAL_TYPES, VALENCE_PLOT_ROW_LEN
from imasyndata_web.plotly_config import PLOT_AXIS_STYLE, \
    FONT, BG_COLOR, BG_COLOR_PLOT, TARGET_COLORS, PRECURSOR_COLORS, GRID_COLOR


def __get_values_counts(data):
    values = list(set(v for v in data))
    amounts = [data.count(x) for x in values]
    amounts = [x / np.linalg.norm(amounts) for x in amounts]

    return values, amounts


def plot_valencies_row(elements, elements_target, elements_precursors):

    elements_to_draw = [el for el in elements if el in elements_target and el in elements_precursors]

    if not elements_to_draw:
        return {}

    cols_num = max(VALENCE_PLOT_ROW_LEN, len(elements_to_draw))
    valence_plot = make_subplots(rows=1,
                                 cols=cols_num,
                                 shared_yaxes=True,
                                 horizontal_spacing=0.005,
                                 subplot_titles=elements_to_draw)

    col = 1
    for el in elements_to_draw:
        t_values, t_amount = __get_values_counts(elements_target[el])
        p_values, p_amount = __get_values_counts(elements_precursors[el])
        x_range = max(t_amount + p_amount) + 0.1 if t_amount + p_amount else 1

        t_bars = go.Bar(x=t_amount,
                        y=t_values,
                        base=[-1 * y for y in t_amount], name=el, meta=el, customdata=[el for el in t_values],
                        width=0.8,
                        orientation='h',
                        marker=dict(color=TARGET_COLORS["bars_marker"],
                                    line=dict(color=TARGET_COLORS["bars_line"],
                                              width=2)))

        p_bars = go.Bar(x=p_amount,
                        y=p_values,
                        name=el, meta=el, customdata=[el for el in p_amount],
                        width=0.8,
                        orientation='h',
                        marker=dict(color=PRECURSOR_COLORS["bars_marker"],
                                    line=dict(color=PRECURSOR_COLORS["bars_line"],
                                              width=2)))

        valence_plot.append_trace(t_bars, row=1, col=col)
        valence_plot.append_trace(p_bars, row=1, col=col)
        xaxes_layout = deepcopy(PLOT_AXIS_STYLE["xaxis"])
        xaxes_layout.update(dict(showgrid=False,
                                 mirror=True,
                                 showticklabels=False,
                                 zeroline=True,
                                 zerolinecolor=GRID_COLOR,
                                 range=[-1 * x_range, x_range],
                                 linewidth=1))
        valence_plot.update_xaxes(xaxes_layout, row=1, col=col)
        valence_plot.update_yaxes(row=1, col=col,
                                  showgrid=True,
                                  zeroline=False,
                                  mirror=True,
                                  linecolor='#000000',
                                  linewidth=1,
                                  dtick=1,
                                  gridcolor = GRID_COLOR
                                  )
        col += 1

    yaxis_style = dict(title='Valence state',
                       title_font=FONT["axis_title"],
                       linecolor="#000000",
                       linewidth=1,
                       tickfont=FONT["axis_ticks"],
                       title_standoff=10,
                       range=[0.5, 6.5]
                       )
    valence_plot.update_yaxes(yaxis_style, row=1, col=1)

    valence_plot.update_annotations(font=FONT["plot_title"])

    valence_plot.update_layout(autosize=True,
                               showlegend=False,
                               margin=dict(t=25, r=5, b=10),
                               height=150,
                               paper_bgcolor=BG_COLOR,
                               plot_bgcolor = BG_COLOR_PLOT,
                               barmode='stack')

    return valence_plot


def serve_layout(elements_target, elements_precursors):
    layout = []
    for t, elements in METAL_TYPES.items():
        valence_plot = plot_valencies_row(elements, elements_target, elements_precursors)
        label_text = " ".join([s.capitalize() for s in t.split("_")])
        if valence_plot:
            layout.append(html.Details([html.Summary(label_text,
                                                     id="valence-row",
                                                     style={"font-weight": "700"}),
                                        html.Div(dcc.Graph(figure=valence_plot,
                                                           id="valence-" + t),
                                                 id="valence-plot",
                                                 style={"align": "center", "margin": "0px", "padding": "0px"})],
                                       open="open",
                                       style={"padding": "10px"}))
    return layout