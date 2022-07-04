from copy import deepcopy

import plotly.graph_objs as go
from plotly.subplots import make_subplots

import dash_html_components as html
import dash_core_components as dcc
from imasyndata_web.constants import SYN_TYPES, SYN_TYPES2COLLECTIONS
from imasyndata_web.plotly_config import SYN_TYPES_COLOR_SCHEME, PLOT_AXIS_STYLE, PLOT_TITLE_STYLE, \
    TARGET_COLORS, BG_COLOR, BG_COLOR_PLOT, FONT


def get_syntypes_piechart(data):
    syntypes_stat = {t: c for t, c in data.items() if "Recipe" in t}
    labels = [" ".join([s.capitalize() for s in t.split("_") if s != "ceramic"]) for t in SYN_TYPES]
    values = [c for t, c in syntypes_stat.items()]

    piechart = go.Pie(labels=labels,
                      values=values,
                      marker={"colors": SYN_TYPES_COLOR_SCHEME})

    layout = deepcopy(PLOT_AXIS_STYLE)
    layout.update(PLOT_TITLE_STYLE)
    layout.update(dict(margin=dict(t=25)))
    layout.update(dict(paper_bgcolor='#d9d9d9',
                       height=350,
                       legend=dict(traceorder="reversed",
                                   font_color="#000000")
                       ))

    return [html.H4("Number of recipes per synthesis type",
                    style={"text-align": "center"}
                    ),
           dcc.Graph(id="recipe-types-db",
                     figure={"data": [piechart],
                             "layout": go.Layout(layout)})]


def get_db_stat_numbers(data):
    total_recipes = sum(c for t, c in data.items() if "v20" in t)
    dois_num = data.get("doi", 0)
    materials_num = data.get("Materials_Data_v20", 0)
    reactions_num = data.get("Reactions_Data_v20", 0)

    def __draw_row(image, title):
        return html.Div([html.Img(src="assets/icons/"+image,
                                  style={"width": "50px", 'display': 'inline-block'},
                                  className="two columns"),
                         html.H4(title,
                                 style={"margin-left": "10px"},
                                 className="ten columns")],
                        className="row",
                        style={"margin-bottom": "20px"})

    return [__draw_row("recipes_50.png", "Total number or recipes: {:,}".format(total_recipes)),
            __draw_row("papers_50.png", "Unique DOIs: {:,}".format(dois_num)),
            __draw_row("materials_50.png", "Materials: {:,}".format(materials_num)),
            __draw_row("reactions_50.png", "Reactions: {:,}".format(reactions_num))]


def get_me_elements_freq_plot(elements_freq, graph_title="", graph_id=""):

    bars = []
    i = 0
    for s_type in SYN_TYPES:
        bars.append(go.Bar(y=[data.get(s_type, 0) for data in elements_freq.values()],
                           x=[el for el in elements_freq.keys()],
                           text=" ".join([s.capitalize() for s in s_type.split("_")[:-2]]),
                           name=" ".join([s.capitalize() for s in s_type.split("_")[:-2]]),
                           marker_color=SYN_TYPES_COLOR_SCHEME[i]))
        i += 1

    layout = go.Layout(title=graph_title,
                       barmode="stack",
                       margin=dict(l=40, r=5, t=5),
                       legend=dict(orientation="h",
                                   traceorder="reversed",
                                   font_color="#000000"))

    layout.update(PLOT_TITLE_STYLE)
    xaxis = deepcopy(PLOT_AXIS_STYLE["yaxis"])
    yaxis = deepcopy(PLOT_AXIS_STYLE["xaxis"])
    yaxis.update(dict(title_text="Amount"))
    xaxis.update(dict(title_text="Me Elements"))
    layout.update(dict(xaxis=xaxis,
                       yaxis=yaxis))
    layout.update(dict(paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT))
    figure = {"data": bars,
              "layout": layout}

    return [html.H4("Distribution of metal elements in materials",
                    style={"text-align": "center"}),
            dcc.Graph(figure=figure,
                      id=graph_id),
            html.Br()]


def get_prec_anions_freq_plot(anion_freq, graph_title="", graph_id=""):

    anions = [a for a in anion_freq.keys()]
    col_num = 7
    row_num = int(len(anion_freq)/col_num) if len(anion_freq)%col_num == 0 else int(len(anion_freq)/col_num) + 1
    specs = [[{"type": "domain"}]*col_num]*row_num
    figure = make_subplots(rows=row_num, cols=col_num,
                           subplot_titles=anions,
                           specs=specs,
                           horizontal_spacing=0.01,
                           vertical_spacing=0.1
                           )

    col = 1
    row = 1
    for anion in anions:
        figure.add_trace(go.Pie(labels=[" ".join([s.capitalize() for s in t.split("_")[:-2]]) for t in SYN_TYPES],
                                values=[anion_freq[anion].get(t, 0) for t in SYN_TYPES],
                                textinfo="none",
                                marker={"colors": SYN_TYPES_COLOR_SCHEME}), row, col)
        if col == col_num:
            col = 1
            row += 1
        else:
            col += 1

    figure.update_annotations(font=FONT["plot_title"])
    figure.update_layout(dict(paper_bgcolor=BG_COLOR,
                              plot_bgcolor=BG_COLOR_PLOT,
                              margin=dict(l=20, r=20, t=20),
                              showlegend=True,
                              height=600,
                              legend=dict(orientation="h",
                                          traceorder="reversed",
                                          font_color="#000000")))


    return [html.H4("Precursors anions per synthesis type",
                    style={"text-align": "center"}),
            dcc.Graph(figure=figure,
                     id=graph_id),
            html.Br()]


def get_temperature_per_syntype_plot(temperature_data, graph_title="", graph_id=""):
    histograms = []
    i = 0
    for s_type in SYN_TYPES:
        temperature = temperature_data.get(SYN_TYPES2COLLECTIONS[s_type], [])
        histograms.append(go.Histogram(x=[t for t in temperature if 10 < t < 1700],
                                       histnorm='probability',
                                       text=" ".join([s.capitalize() for s in s_type.split("_")[:-2]]),
                                       name=" ".join([s.capitalize() for s in s_type.split("_")[:-2]]),
                                       marker_color=SYN_TYPES_COLOR_SCHEME[i]))
        i += 1

    layout = go.Layout(title=graph_title,
                       margin=dict(l=45, r=5, t=5),
                       legend=dict(orientation="h",
                                   traceorder="reversed",
                                   font_color="#000000")
                       )

    layout.update(PLOT_TITLE_STYLE)
    xaxis = deepcopy(PLOT_AXIS_STYLE["xaxis"])
    yaxis = deepcopy(PLOT_AXIS_STYLE["yaxis"])
    yaxis.update(dict(title_text="Probability",
                      showgrid=True))
    xaxis.update(dict(title_text="Temperature, C",
                      showgrid=False))
    layout.update(dict(xaxis=xaxis,
                       yaxis=yaxis))
    layout.update(dict(paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT))
    figure = {"data": histograms,
              "layout": layout}

    return [html.H4("Distribution of firing temperatures",
                    style={"text-align": "center"}),
            dcc.Graph(figure=figure,
                     id=graph_id),
            html.Br()]