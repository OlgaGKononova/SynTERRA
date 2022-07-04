# coding=utf-8
import dash_core_components as dcc
import dash_html_components as html

"""
Defining the core view (layout) component for the entire app.
Please do not define any callback logic in this file.
"""


header_layout = [dcc.Location(id="url", refresh=False),
                 html.Div([html.Div([#html.H1("Inorganic Materials Synthesis (IMaSyn) Project"),
                                     html.Div("\"Explore the power of words in...\"", className="subtitle"),
                                     html.Div([html.H1("SynTERRA: ",
                                                       className="two columns",
                                                       style={"margin": "0px", "padding": "0px",
                                                              "width": "200px",
                                                              #"border": "1px solid black"
                                                              }
                                                       ),
                                               html.H1("Synthesis Text-Extracted `Recipes' Repository & Analyser",
                                                       className="ten columns",
                                                       style={"marginLeft": "15px",
                                                              "marginRight": "0px",
                                                              "font-size": "3.8rem",
                                                              "paddingTop": "13px",
                                                              "paddingRight": "13px",
                                                              #"width": "800px",
                                                              #"border": "1px solid black"
                                                              }
                                                       )],
                                              className="row"
                                              )],
                                   className="ten columns"),
                           html.Img(src="assets/CederGroup.png",
                                    className="two columns",
                                    style={#"width": 250,
                                           "align": "right"})],
                          className="row"),
                 html.Div(html.Nav([dcc.Link("Papers Statistics", href="/papers_stats"),
                                    html.Span(" | "),
                                    dcc.Link("Dataset Statistics", href="/data_stats"),
                                    html.Span(" | "),
                                    dcc.Link("Explore", href="/search"),
                                    html.Span(" | "),
                                    dcc.Link("About", href="/about")
                                    #dcc.Link("SynCheck", href="http://lb.syncheck.production.svc.spin.nersc.org/"),
                                    ],
                                   id="nav-bar",
                                   className="row",
                                   style={"margin": "20px",
                                          "margin-left": "155px"}))]


footer_layout = [html.Div(["Designed by ",
                           html.A("Olga Kononova", href="https://olgakononova.com/"), html.Br(),
                           "IMaSyn Project © 2021, ",
                           html.A("CEDER Research Group", href="http://ceder.berkeley.edu/"), html.Br(),
                           "University of California Berkeley & "
                           "Lawrence Berkeley National Laboratory, Berkeley, CA, USA"],
                          className="nine columns",
                          style={"font-size": "12px"}),
                 html.Div([html.A("Send your questions and feedback", href="mailto:cedergroup-ml-team@lbl.gov"),
                           html.Div([html.Br(),
                                     "Powered by ",
                                     html.A("Plotly Dash", href="https://dash.plotly.com/"),
                                     " via ",
                                     html.A("SPIN (NERSC)", href="https://www.nersc.gov/systems/spin/")],
                                     style={"font-size": "12px"})],
                          className="three columns")]

def core_view_html():
    return html.Div([html.Div(header_layout,
                              id="page-header"
                              ),
                     html.Div(id="page-content",
                              className="container",
                              ),
                     html.Div(footer_layout,
                              className="row footer")])
