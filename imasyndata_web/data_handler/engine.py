import dash_core_components as dcc
import dash_html_components as html

from imasyndata_web.constants import VALENCE_LBL_TITLE
from imasyndata_web.data_handler.wordcloud.logic import build_application_content
from imasyndata_web.data_handler.targets.logic import build_targets_content, build_targets_elem_stats
from imasyndata_web.data_handler.precursors.logic import build_precursors_content, build_precursors_elem_stats
from imasyndata_web.data_handler.valence.logic import build_valence_content
from imasyndata_web.data_handler.operations.logic import \
    build_operations_content, draw_operations_graph, draw_operation_attributes, draw_operation_precursors
from imasyndata_web.data_handler.thermo.logic import build_materials_thermo_content


class DataVisualizationEngine():
    def __init__(self):
        pass

    @staticmethod
    def render_content(tab):
        content_map = {"tab-application": html.Div("", id="tab-application-content", className="row"),
                       "tab-targets": html.Div("", id="tab-targets-content", className="row"),
                       "tab-precursors": html.Div("", id="tab-precursors-content", className="row"),
                       "tab-ftemps": html.Div("", id="tab-ftemps-content"),
                       "tab-operations": html.Div("", id="tab-operations-content", className="row"),
                       "tab-thermo": html.Div("", id="tab-thermo-content"),
                       "tab-MP": html.Div("", id="tab-MP-content"),
                       "tab-valence": html.Div("", id="tab-valence-content")}
        return content_map[tab]

    @staticmethod
    def render_tab_application_content(data_table):
        return build_application_content(data_table)

    @staticmethod
    def render_tab_targets_content(data_table):
        targets_plot, checkbox, checkbox_lbl = build_targets_content(data_table)

        check_list = [html.Label(checkbox_lbl, id='targets-elements-choice_lbl', style={'margin-top': '15px'}),
                      html.Div(dcc.Checklist(id='targets-elements-choice_chk',
                                             options=checkbox,
                                             value=[],
                                             labelStyle={'display': 'block'},
                                             style={'columnCount': 2}))]

        return [html.Div(targets_plot, id="targets-stats_plot", className="five columns"),
                html.Div(check_list, id="targets-elem-choice", className="two columns"),
                html.Div("", id="targets-elem-stats_plot", className="five columns")]

    @staticmethod
    def update_targets_elem_stats_plot(data_table, chosen_elements):
        return build_targets_elem_stats(data_table, chosen_elements)

    @staticmethod
    def render_tab_precursors_content(data_table):
        precursors_plot, checkbox, checkbox_lbl = build_precursors_content(data_table)

        check_list = [html.Label(checkbox_lbl, id='precursors-elements-choice_lbl', style={'margin-top': '15px'}),
                      html.Div(dcc.Checklist(id='precursors-elements-choice_chk',
                                             options=checkbox,
                                             value=[],
                                             labelStyle={'display': 'block'},
                                             style={'columnCount': 2}))]

        return [html.Div(precursors_plot, id="precursors-stats_plot", className="five columns"),
                html.Div(check_list, id="precursors-elem-choice", className="two columns"),
                html.Div("", id="precursors-elem-stats_plot", className="five columns")]

    @staticmethod
    def update_precursors_elem_stats_plot(data_table, chosen_elements):
        return build_precursors_elem_stats(data_table, chosen_elements)

    @staticmethod
    def render_valence_content(data_table):
        valence_plot = build_valence_content(data_table)
        return [html.Br(),
                html.Label(VALENCE_LBL_TITLE),
                html.Div(valence_plot, id="valence-stats_plot")]

    @staticmethod
    def render_firing_conditions_content(data_table):
        return [html.Div(id="ftemps-stats_plot", className="row"),
                html.Div("", id="filtered-reactions_table")]

    @staticmethod
    def render_operations_content(data_table):
        # row is split into two halfs:
        # left is the graph, right is the attributes
        layout = build_operations_content(data_table)
        return layout

    @staticmethod
    def update_synthesis_graph(data_table, threshold):
        graph_elements, graph_style, _, _ = draw_operations_graph(data_table, threshold)
        return graph_elements, graph_style

    @staticmethod
    def display_operation_attributes(data_table, operation):
        attributes_graph, attributes_lbl = draw_operation_attributes(data_table, operation)
        return attributes_graph, attributes_lbl

    @staticmethod
    def display_operation_precursors(data_table, edge):
        precursors_graph, precursors_lbl = draw_operation_precursors(data_table, edge)
        return precursors_graph, precursors_lbl

    @staticmethod
    def render_thermo_content(data_table):
        return [html.Div([dcc.Tabs(id="thermo-output_tabs", value='thermo-tab-material',
                                   children=[dcc.Tab(label="Formation/Decomposition energy per material",
                                                     value='thermo-tab-material', className='search-tab',
                                                     selected_className='search-tab--selected'),
                                             dcc.Tab(label="Reaction energy",
                                                     value='thermo-tab-reactions', className='search-tab',
                                                     selected_className='search-tab--selected')
                                             ]),
                          html.Div(id="thermo-output-content")], className="row")]


    @staticmethod
    def render_thermo_tab_content(tab):
        slider = html.Div([html.Label("Setup temperature value:", style={'font-weight': '700'}),
                           dcc.Slider(id='temperature_slider',
                                      min=0, max=2000, value=0, step=100,
                                      marks={300 + i * 100: '{}'.format(300 + i * 100) for i in range(18)})],
                          className="row")

        content_map = {"thermo-tab-dist": html.Div([html.Br(),
                                                    slider,
                                                    html.Br(),
                                                    html.Div("", id="thermo-tab-dist-content", className="row")]),
                       "thermo-tab-material": html.Div([html.Br(),
                                                        slider,
                                                        html.Br(),
                                                        html.Div([html.Label("Sort by:"),
                                                                  dcc.RadioItems(id='sorting-energies_ri',
                                                                                 options=[{'label': 'av. formation energy',
                                                                                           'value': 'Hf'},
                                                                                          {'label': 'av. decomposition energy',
                                                                                           'value': 'Hd'}],
                                                                                 value='Hf',
                                                                                 labelStyle={'display': 'inline-block'})]),
                                                        html.Div("", id="thermo-tab-material-content", className="row"),
                                                        ]),
                       "thermo-tab-reactions": html.Div([html.Br(),
                                                         slider,
                                                         html.Br(),
                                                         html.Div("", id="thermo-tab-reactions-content")]),
                       }

        return content_map[tab]

    @staticmethod
    def render_thermo_tab_material_content(search_data, temp_value, sorting_flag):
        return build_materials_thermo_content(search_data, temp_value, sorting_flag)

    def render_MP_content(self, data_table):
        return []


dve = DataVisualizationEngine()