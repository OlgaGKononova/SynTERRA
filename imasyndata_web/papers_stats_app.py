import dash_html_components as html
import dash_core_components as dcc
from imasyndata_web.papers_stats.components import get_histogram_of_publishers
from imasyndata_web.papers_stats.publishers_stats import get_publishers

"""
Layout of the papers statistics
"""


layout = [html.Div([html.Br(),
                    dcc.Dropdown(id="publisher_select",
                                options=[{"label": p, "value": p} for p in get_publishers()],
                                value=None,
                                placeholder='Filter by Publisher')],
                   style={"width": "270px", "margin": "20px"}),
          html.Div([html.Div(get_histogram_of_publishers(),
                             id="publishers_graph",
                             className="six columns"),
                    html.Div(html.Div(id="recipe-types_graph",
                                      className="six columns"))],
                   className="row")]




