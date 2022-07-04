# -*- coding: utf-8 -*-

import dash
from dash.dependencies import ClientsideFunction, Input, Output, State
import flask
from flask_caching import Cache

import json
import random as rnd
import pandas as pd

from imasyndata_web.core_view import core_view_html
from imasyndata_web import papers_stats_app, search_app, data_stats_app, about
from imasyndata_web.papers_stats.publishers_stats import acronym2publisher
from imasyndata_web.papers_stats.components import get_piechart_per_publisher

from imasyndata_web.search.logic import get_recipes, select_data
from imasyndata_web.search.components import export_button
from imasyndata_web.constants import DEFAULT_TABLE_COLUMNS

from imasyndata_web.utils import generate_download_link
from dash_extensions.snippets import send_data_frame

from imasyndata_web.data_handler.engine import dve

from pprint import pprint

"""
A safe place for the dash app core instance to hang out.
Also, all high level logic for every callback in the entire dash app.
Please do not define any html-returning functions in this file. Import them
from modules like common, view, or an app"s view submodule.
Please see CONTRIBUTING.md before editing this file or callback element ids.
"""

################################################################################
# Dash app core instance
################################################################################
# Any external js scripts you need to define.
# external_scripts = [
#     #"https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"
#     "https://fonts.googleapis.com/css2"
# ]

server = flask.Flask(__name__)
app = dash.Dash(__name__, assets_folder="assets/", server=server)


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "SynTERRA"

app.layout = core_view_html()
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/papers_stats":
        return papers_stats_app.layout
    elif pathname == "/data_stats":
        return data_stats_app.layout
    elif pathname == "/about":
        return about.layout
    elif pathname == "/search":
        return search_app.serve_layout()
    else:
        return papers_stats_app.layout


@app.callback(
    Output("publisher_select", "value"),
    [Input("publishers", "clickData")])
def display_publisher(click_data):
    if click_data is not None:
        publisher = acronym2publisher()[click_data["points"][0]["y"]]
        return publisher
    else:
        return ""


@app.callback(
    Output("recipe-types_graph", "children"),
    [Input("publisher_select", "value")])
def get_recipe_types(publisher):
    return get_piechart_per_publisher(publisher)


@app.callback(
    [Output("search-results_table", "data"),
     Output("search-count_lbl", "children"),
     Output("search-results_table", "columns"),
     Output("export_btn", "disabled"),
     Output("syntypes_graph", "children"),
     Output("query-error_div", "children")],
    [Input("search_btn", "n_clicks")],
    [State("search_input", "value"),
     State("search-database_chk", "value"),
     State("output-columns_chk", "value")])
def search_recipes(n_clicks, search_text, search_collections, additional_columns):

    if n_clicks and search_text:
        output_data, columns, syntypes_bar, error = get_recipes(search_text, search_collections, additional_columns)
        l_data = len(output_data)
        if output_data:
            l_unique_doi = len(set(d["doi"] for d in output_data))
            l_unique_targets = len(set(d["target"] for d in output_data))
            count_lbl = "Found {} recipes from {} DOIs with {} unique targets:"\
                .format(l_data, l_unique_doi, l_unique_targets)
            return output_data, count_lbl, columns, False, syntypes_bar, ""
        elif error:
            return [{}], "", DEFAULT_TABLE_COLUMNS, True, "", "Error: {}".format(error)
        else:
            return [{}], "No recipes found", DEFAULT_TABLE_COLUMNS, True, "", ""
    return [{}], "", DEFAULT_TABLE_COLUMNS, True, "", ""


@app.callback(
    Output("output-content", "children"),
    [Input("output_tabs", "value")])
def render_content(tab):
    return dve.render_content(tab)


@app.callback(
    Output("tab-application-content", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows")])
def render_tab_application_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    if search_data != [{}]:
        return dve.render_tab_application_content(search_data)
    return []


@app.callback(
    Output("tab-targets-content", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows")])
def render_tab_targets_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.render_tab_targets_content(search_data)


@app.callback(
    Output("targets-elem-stats_plot", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows"),
     Input("targets-elements-choice_chk", "value")])
def update_targets_elem_stats_plot(search_data, selected_row_indices, element):
    search_data = select_data(search_data, selected_row_indices)
    return dve.update_targets_elem_stats_plot(search_data, element)


@app.callback(
    Output("tab-precursors-content", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows")])
def render_precursors_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.render_tab_precursors_content(search_data)


@app.callback(
    Output("precursors-elem-stats_plot", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows"),
     Input("precursors-elements-choice_chk", "value")])
def update_precursor_elem_stats_plot(search_data, selected_row_indices, element):
    search_data = select_data(search_data, selected_row_indices)
    return dve.update_precursors_elem_stats_plot(search_data, element)


@app.callback(
    Output("tab-valence-content", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows")])
def render_valence_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.render_valence_content(search_data)


@app.callback(
    Output("tab-operations-content", "children"),
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows")])
def render_operations_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.render_operations_content(search_data)


@app.callback(
    [Output("cytoscape-pane", "elements"),
     Output("cytoscape-pane", "stylesheet")],
    [Input("search-results_table", "data"),
     Input("search-results_table", "selected_rows"),
     Input("threshold_slider", "value")])
def display_operations_graph(search_data, selected_row_indices, threshold):
    search_data = select_data(search_data, selected_row_indices)
    return dve.update_synthesis_graph(search_data, threshold)


@app.callback(
    Output("cytoscape-pane", "generateImage"),
    [Input("export_graph_btn", "n_clicks")])
def export_graphe(n_clicks):
    output = {"type": None,
              "action": "store"}
    if n_clicks:
        output["type"] = "png"
        output["action"] = "download"
    return output


@app.callback(
    [Output("operations-attributes_plot", "children"),
     Output("operations-attributes_sum", "children")],
    [Input("cytoscape-pane", "tapNodeData")],
    [State("search-results_table", "data"),
     State("search-results_table", "selected_rows")])
def display_operations_attributes(operation, search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.display_operation_attributes(search_data, operation)


@app.callback(
    [Output("precursors-attributes_plot", "children"),
     Output("precursors-attributes_sum", "children")],
    [Input("cytoscape-pane", "tapEdgeData")],
    [State("search-results_table", "data"),
     State("search-results_table", "selected_rows")])
def display_graph_edge_data(edge, search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    return dve.display_operation_precursors(search_data, edge)


@app.callback(
    Output("tab-thermo-content", "children"),
    [Input('search-results_table', 'data'),
     Input('search-results_table', 'selected_rows')])
def render_thermo_content(search_data, selected_row_indices):
    search_data = select_data(search_data, selected_row_indices)
    if search_data != [{}]:
        return dve.render_thermo_content(search_data)
    return []


@app.callback(
    Output("thermo-output-content", "children"),
    [Input("thermo-output_tabs", "value")])
def render_thermo_tab_content(tab):
    return dve.render_thermo_tab_content(tab)


@app.callback(
    Output("thermo-tab-material-content", "children"),
    [Input('search-results_table', 'data'),
     Input('search-results_table', 'selected_rows'),
     Input('temperature_slider', 'value'),
     Input('sorting-energies_ri', 'value')])
def render_thermo_tab_material_content(search_data, selected_row_indices, temp_value, sorting_flag):
    search_data = select_data(search_data, selected_row_indices)
    return dve.render_thermo_tab_material_content(search_data, temp_value, sorting_flag)


@app.callback(
    Output("export_tbl", "data"),
    [Input("export_btn", "n_clicks")],
    [State("search-results_table", "data")])
def export_results(n_clicks, data):
    if data and n_clicks:
        output_data = [{k: v for k, v in d.items() if k[0] != "_"} for d in data]
        return send_data_frame(pd.DataFrame(output_data).to_excel, "table.xls", index=False)




