import plotly
import plotly.graph_objs as go

import dash_core_components as dcc
import dash_html_components as html

from imasyndata_web.plotly_config import \
    TARGET_COLORS, PLOT_TITLE_STYLE, PLOT_AXIS_STYLE, FONT, BG_COLOR, BG_COLOR_PLOT, ENERGY_COLORS

from pprint import pprint
from copy import deepcopy


def plot_material_energies(material_data, graph_id):
    hf_data, hd_data, hf_values, hd_values = [], [], [], []
    max_len = max([len(k) for k, v in material_data])

    for num, (formula_id, data) in enumerate(material_data):
        x = [d['Hf'] for d in data]
        hf_values.extend(x)
        hf_data.append(go.Box(x=x,
                              name=formula_id,
                              marker_color=ENERGY_COLORS["pos"] if np.mean(x) > 0 else ENERGY_COLORS["neg"]
                              ))
        x = [d['Hd'] * 10.0 for d in data]
        hd_values.extend(x)
        hd_data.append(go.Box(x=x,
                              name=formula_id,
                              marker_color=ENERGY_COLORS["pos"] if np.mean(x) > 0 else ENERGY_COLORS["neg"]
                              ))

    row_heights = [500] + [200]*len(hf_data)

    energy_plots = make_subplots(rows=len(hf_data) + 1, cols=2, shared_xaxes=True, vertical_spacing=0.0,
                                 horizontal_spacing=0.1, row_heights=row_heights,
                                 subplot_titles=["Energy of formation", "Energy of decomposition"] +
                                                ["" for i in range(len(hf_data))])

    plotting_data = [{'data': hf_data, 'axis_title': 'Energy, eV/atom'},
                     {'data': hd_data, 'axis_title': 'Energy, eV/atom*10'}]

    #energy_plots.append_trace(plot_histogram(hf_values, [128, 0, 128]), 1, 1)
    #energy_plots.append_trace(plot_histogram(hd_values, [128, 0, 128]), 1, 2)
    for col_num in [0, 1]:
        for n in range(len(hf_data)):
            energy_plots.append_trace(plotting_data[col_num]['data'][n], n + 2, col=col_num + 1)
            energy_plots.update_yaxes(PLOT_AXIS_STYLE, showgrid=True, row=n + 2, col=col_num + 1)

        energy_plots.update_xaxes(PLOT_AXIS_STYLE, showgrid=True, row=1, col=col_num + 1)
        energy_plots.update_yaxes(PLOT_AXIS_STYLE, showgrid=True, row=1, col=col_num + 1)
        energy_plots.update_xaxes(PLOT_AXIS_STYLE, title=plotting_data[col_num]['axis_title'],
                                  row=len(hf_data) + 1, col=col_num + 1)

    energy_plots.update_layout(autosize=True, showlegend=False,
                               margin=dict(l=max_len * 6.5, t=80),
                               height=600 if len(material_data) < 30 else len(material_data) * 10,
                               titlefont=PLOT_TITLE_STYLE,
                               xaxis=dict(showgrid=True, linecolor='#000000', linewidth=2),
                               yaxis=dict(linecolor='#000000', linewidth=2,
                                          #tickfont=self.__tickfont,
                                          showgrid=True))

    return dcc.Graph(id=graph_id, figure=energy_plots)