from copy import deepcopy

import plotly.graph_objs as go

import dash_html_components as html
import dash_core_components as dcc

from imasyndata_web.constants import PUB_STAT_PATH
from imasyndata_web.plotly_config import PUB_COLOR_SCHEME, SYN_TYPES_COLOR_SCHEME, \
    PLOT_AXIS_STYLE, PLOT_TITLE_STYLE, BG_COLOR, BG_COLOR_PLOT
from imasyndata_web.papers_stats.publishers_stats import publisher2acronym, get_publisher_data, get_recipes_stat


LINE_COLOR = "rgba(58, 71, 80, 0.75)"


def get_histogram_of_publishers():
    publishers = sorted(get_publisher_data(PUB_STAT_PATH).items(), key=lambda kv: kv[1]["nr_of_HTML"], reverse=False)
    pubs = [publisher2acronym().get(p, p) for p, c in publishers]
    parsed_per_pub = [c["nr_of_HTML"] for p, c in publishers]
    missed_per_pub = [c["nr_of_HTML"]-c["nr_of_parsed"] for p, c in publishers]
    nr_papers = sum([c["nr_of_HTML"] for p, c in publishers])
    nr_htmls = sum([c["nr_of_parsed"] for p, c in publishers])
    title = "{:,} parser papers".format(nr_papers) + " / " + "{:,} HTMLs".format(nr_htmls)
    style={"text-align": "center",
           "margin-bottom": "20px"}

    parsed_papers_bar = go.Bar(y=pubs,
                               x=parsed_per_pub,
                               marker=dict(color=PUB_COLOR_SCHEME,
                                           line=dict(color=LINE_COLOR,
                                                     width=1)),
                               orientation="h")
    missed_papers_bar = go.Bar(y=pubs,
                               x=missed_per_pub,
                               marker=dict(color=PUB_COLOR_SCHEME,
                                           opacity=0.5,
                                           line=dict(color=LINE_COLOR,
                                                     width=1)),
                               orientation="h")

    layout = deepcopy(PLOT_AXIS_STYLE)
    #layout["xaxis"].update(dict(gridcolor="#d9d9d9"))
    layout["yaxis"].update(dict(showgrid=False))
    layout.update(dict(margin=dict(t=10)))
    layout.update(dict(showlegend=False,
                       barmode="stack",
                       paper_bgcolor=BG_COLOR,
                       plot_bgcolor=BG_COLOR_PLOT
                       ))

    return [html.H4(title, style=style),
            html.P( "Click bar to see statistics per publisher", style={"font-style": "italic",
                                                                        "marginTop": "0px",
                                                                        "marginBottom": "0px",
                                                                        "font-size": "11px"}),
            dcc.Graph(id="publishers",
                     figure={"data": [parsed_papers_bar, missed_papers_bar],
                             "layout": go.Layout(layout)})]


def __label2text(label):
    return label.replace("_", " ").capitalize()


def get_piechart_per_publisher(publisher):
    not_show_list = ["something_else"]
    recipes_stat = get_recipes_stat(publisher)
    nr_papers = recipes_stat["nr_of_parsed"]
    syn_types_count = recipes_stat["syn_types_count"]
    nr_recipes = sum([v for r, v in syn_types_count.items()])

    labels = [__label2text(t) for t in syn_types_count.keys() if t not in not_show_list]
    values = [c for t, c in syn_types_count.items() if t not in not_show_list]
    subtitle = "({:,} w. synthesis recipes)".format(nr_recipes) if publisher else html.Br()
    title = "{:,} {} publications ".format(nr_papers, publisher if publisher else "total")

    piechart = go.Pie(labels=labels,
                      values=values,
                      marker={"colors": SYN_TYPES_COLOR_SCHEME})

    layout = deepcopy(PLOT_AXIS_STYLE)
    layout.update(dict(margin=dict(t=10)))
    layout.update(dict(paper_bgcolor=BG_COLOR,
                       legend=dict(orientation="h",
                                   traceorder="reversed",
                                   font_color="#000000")
                       ))

    return [html.H4([title, html.Br(), subtitle], style={"text-align": "center"}),
            html.P("", style={"font-style": "italic", "margin": "0px"}),
            dcc.Graph(id="recipe-types",
                     figure={"data": [piechart],
                             "layout": go.Layout(layout)})]
