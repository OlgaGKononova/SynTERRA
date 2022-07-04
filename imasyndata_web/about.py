import json

import dash_core_components as dcc
import dash_html_components as html


about_text = "Inorganic Materials Synthesis Project is the largest collection of materials synthesis \"recipes\" " \
             "publicly available for data mining and machine learning. " \
             "The \"recipes\" were extracted and compiled from ~5M scientific publications using state-of-the-art " \
             "text mining and natural language processing approaches. "


def __make_card(name, bio, image, link):
    return html.Div([html.Img(src="assets/ppl/"+image,
                              style={"width": "150px", 'display': 'inline-block'},
                              className="two columns"),
                              html.Div([html.A(name, href=link),
                                        html.Br(),
                                        bio],
                                       style={'display': 'inline-block',
                                              "font-size": "13px"},
                                       className="eight columns")],
                    className="row",
                    style={"border": "1px solid #F19F4D",
                            "padding": "7px",
                            "width": "500px",
                            "height": "190px",
                            'display': 'inline-block',
                            "background-color": "#f2f2f2",
                            "margin": "10px"
                            })


people = json.loads(open("imasyndata_web/static/people.json").read())


layout = [html.Div([about_text,
                    "The detailed description of data extraction and processing can be found in ",
                    html.A("Kononova et al. Scientific Data 2019",
                           href="https://www.nature.com/articles/s41597-019-0224-1"),
                    ". Dataset in json format is available on ",
                    html.A("github",
                           href="https://github.com/CederGroupHub/text-mined-synthesis_public"),
                    ]),
          html.H5("Our team"),
          html.Div([__make_card(d["name"], d["bio"], d["image"], d["link"]) for d in people],
                    style={"align": "center"}
                   ),
          html.H5("Acknowledgement"),
          html.Div(["We thank former CEDER Group members ",
                    html.A("Dr. Vahe Tshitoyan", href="https://vtshitoyan.github.io/"),
                    " and ",
                    html.A("Dr. Ziqin Rong", href="https://github.com/shaunrong"),
                    " for the initial idea about the web app and help with the papers scraping",
                    html.Br(),
                    "Text and data mining agreements with the publishers were negotiated by "
                    "Ms. Anna Sackmann (Data Services Librarian, UC Berkeley), "
                    "Ms. Rachael Samberg (Scholarly Communication Officer, UC Berkeley), "
                    "Mr. Timothy Vollmer (Scholarly Communication & Copyright Librarian, UC Berkeley).",
                    html.Br(),
                    "Initial processing of HTML content was performed in collaboration with the group of ",
                    html.A("Prof. Elsa Olivetti", href="https://olivetti.mit.edu/"),
                    ".",
                    html.Br()]),
          html.H5("Funding"),
          html.Div([html.A("Energy & Biosciences Institute",
                           href="https://vcresearch.berkeley.edu/research-unit/energy-biosciences-institute"),
                    " through the EBI-Shell program (Award No. PT74140 and PT78473).",
                    html.Br(),
                    "Office of Naval Research (Award #N00014-14-1-0444).",
                    html.Br(),
                    "National Science Foundation (Grant No. 1534340)",
                    html.Br(),
                    "The Assistant Secretary of Energy Efficiency and Renewable Energy, "
                    "Vehicle Technologies Office, U.S. Department of Energy (Contract #DE-AC02-05CH11231)."])
          ]