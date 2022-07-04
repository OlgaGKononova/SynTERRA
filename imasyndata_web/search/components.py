from copy import deepcopy

import plotly
import plotly.graph_objs as go

import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

from imasyndata_web.constants import INPUT_PLACEHOLDER, DEFAULT_TABLE_COLUMNS, TABLE_COLUMNS_WIDTH
from imasyndata_web.plotly_config import SYN_TYPES_COLOR_SCHEME, PLOT_TITLE_STYLE, PLOT_AXIS_STYLE, \
    FONT, BG_COLOR, BG_COLOR_PLOT, GRID_COLOR


input_layout = html.Div([html.Div(dcc.Input(id="search_input",
                                            type="text",
                                            autoFocus=True,
                                            placeholder=INPUT_PLACEHOLDER,
                                            style={"width": "100%"}),
                                  className="ten columns"),
                         html.Div(html.Button("Find Recipes",
                                              className="button-primary",
                                              id="search_btn"),
                                  style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "5px"},
                                  className="two columns")],
                        className="row",
                        style={"display": "table", "margin-top": "0px", "width": "100%"})


tabs_layout = html.Div([dcc.Tabs(id="output_tabs",
                                 value='tab-targets',
                                 children=[dcc.Tab(label="Targets Statistics",
                                                   value='tab-targets',
                                                   className='search-tab',
                                                   selected_className='search-tab--selected'),
                                           dcc.Tab(label="Precursors Statistics",
                                                   value='tab-precursors',
                                                   className='search-tab',
                                                   selected_className='search-tab--selected'),
                                           dcc.Tab(label="Oxidation State",
                                                   value='tab-valence',
                                                   className='search-tab',
                                                   selected_className='search-tab--selected'),
                                           # dcc.Tab(label="Firing conditions",
                                           #         value='tab-ftemps',
                                           #         className='search-tab',
                                           #         selected_className='search-tab--selected'),
                                           dcc.Tab(label="Synthesis Flowchart",
                                                   value='tab-operations',
                                                   className='search-tab',
                                                   selected_className='search-tab--selected'),
                                           dcc.Tab(label="Learn more",
                                                   value='tab-application',
                                                   className='search-tab',
                                                   selected_className='search-tab--selected'),
                                           # dcc.Tab(label="Thermochemical Data",
                                           #         value='tab-thermo',
                                           #         className='search-tab',
                                           #         selected_className='search-tab--selected'),
                                           # dcc.Tab(label="Materials Project",
                                           #         value='tab-MP',
                                           #         className='search-tab',
                                           #         selected_className='search-tab--selected')
                                           ]),
                        html.Div(id="output-content",
                                 style={"margin-bottom": "100px"})]
                       )


def draw_table():
    return dcc.Loading(dt.DataTable(id='search-results_table',
                                    columns=DEFAULT_TABLE_COLUMNS,
                                    data=[{c["id"]: "" for c in DEFAULT_TABLE_COLUMNS}],
                                    row_selectable="multi",
                                    editable=False,
                                    filter_action="none",
                                    sort_action="native",
                                    sort_mode = "multi",
                                    fixed_rows={"headers": True, "data": 0},
                                    #selected_row_ids=[],
                                    selected_rows = [],
                                    #style_as_list_view=True,
                                    style_data={'whiteSpace': 'normal'},
                                    style_cell={
                                        'padding': '5px',
                                        'textAlign': 'center',
                                        'whiteSpace': 'normal',
                                        "background-color": BG_COLOR_PLOT,
                                        "border-color": GRID_COLOR
                                        },
                                    style_header={
                                        'backgroundColor': "#94ba4a", #'#f9cf00',
                                        'fontWeight': 'bold'
                                    },
                                    style_table={
                                        'maxHeight': 300,
                                        'overflowY': 'scroll',
                                        #'border': "1px solid lightgrey"
                                        #'width': '95%'
                                    },
                                    style_data_conditional=TABLE_COLUMNS_WIDTH,
                                    virtualization=True),
                       type="dot",
                       color="#F19F4D",
                       style={"background": "none"})


export_button = [html.Button("Export table",
                             className="button-primary",
                             id="export_btn"),
                 html.A(id='download-link',
                        download="",
                        href="",
                        target="_blank")]


def syntypes_stats_plot(data):

    syntypes_bars = []
    total_num = 0
    for i, (t, count) in enumerate(data.items()):
        total_num += count
        syntypes_bars.append(go.Bar(x=[count],
                                    y=[""],
                                    text=t,
                                    marker_color=SYN_TYPES_COLOR_SCHEME[i],
                                    orientation="h",
                                    hoverinfo='skip',
                                    textposition='auto',
                                    textfont_color="black"
                                    ))

    layout = go.Layout(barmode="stack",
                       paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT,
                       height=30,
                       showlegend=False,
                       xaxis=dict(visible=False,
                                  range=[0,total_num]),
                       yaxis=dict(visible=False),
                       margin=dict(l=0, r=0, t=0, b=0)
                       )

    figure = {"data": syntypes_bars,
              "layout": layout}

    return dcc.Graph(figure=figure,
                     id="syntypes-graph")

