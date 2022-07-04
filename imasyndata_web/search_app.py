import dash_html_components as html
import dash_core_components as dcc
from dash_extensions import Download

from imasyndata_web.search.cheatsheet import cheatsheet
from imasyndata_web.search.components import tabs_layout, input_layout, draw_table
from imasyndata_web.constants import COLLECTIONS_OPTIONS, EXT_COLUMNS_OPTIONS


def serve_layout():
    """Generates the layout dynamically on every refresh"""
    return [html.Br(),
            html.Div(" ", id="query-error_div", className="row", style={"color": "red"}),
            input_layout,
            html.P("\n\n"),
            html.Details([html.Summary("Show query language \"cheat-sheet\""),
                          html.Div(cheatsheet(),
                                   style={"marginTop": "10px",
                                          "paddingLeft": "30px",
                                          "font-size": "10px"})]),
            html.Br(style={"margin": "0px", "padding": "0px"}),
            html.Div([html.Label("Reactions databases to query:", style={"font-weight": "700"}),
                      dcc.Checklist(id="search-database_chk",
                                    options=COLLECTIONS_OPTIONS,
                                    value=[d["value"] for d in COLLECTIONS_OPTIONS],
                                    labelStyle={"display": "inline-block"})]),
            html.Br(style={"margin": "0px", "padding": "0px"}),
            html.Div([html.Div([html.Label("Show additional columns:",
                                           style={"font-weight": "700"}),
                                dcc.Checklist(id="output-columns_chk",
                                              options=EXT_COLUMNS_OPTIONS,
                                              value=[],
                                              labelStyle={"display": "inline-block"})],
                               className="ten columns"),
                      # export_btn
                      html.Div([html.Button("Export table",
                                            className="button-primary",
                                            id="export_btn",
                                            disabled=True),
                                Download(id="export_tbl")],
                                id="export_div",
                                className="two columns",
                                style={"padding": "0px", "marginRight": "0px"})],
                     className="row",
                     style={"width": "100%"}),
            html.Br(style={"margin": "0px", "padding": "0px"}),
            html.Div([html.Div(html.Label("", id="search-count_lbl"),
                               className="row",
                               style={"paddingBottom": "10px", "marginTop": "0px"}
                               ),
                      html.Div(id="syntypes_graph",
                               className="row"),
                      html.Div(draw_table(),
                               id="search-results",
                               className="row",
                               style={"height": "100%"})]),
            html.Hr(style={"border-width": "2px"}),
            tabs_layout]
