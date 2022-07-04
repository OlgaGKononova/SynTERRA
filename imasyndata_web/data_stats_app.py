import dash_html_components as html
import dash_core_components as dcc

from imasyndata_web.data_stats.components import get_syntypes_piechart, get_db_stat_numbers, get_me_elements_freq_plot, \
    get_temperature_per_syntype_plot, get_prec_anions_freq_plot
from imasyndata_web.data_stats.database_stats import load_stat_data
from imasyndata_web.constants import DB_STAT_PATH, MATERIALS_STAT_PATH, RECIPES_STAT_PATH
#from imasyndata_web.db_stats.analysis_tools import analyze_materials


dataset_stat = load_stat_data(DB_STAT_PATH)
materials_stat = load_stat_data(MATERIALS_STAT_PATH)
recipes_stat = load_stat_data(RECIPES_STAT_PATH)

layout = [html.Div([html.Div(get_db_stat_numbers(dataset_stat),
                             className="six columns"),
                    html.Div(get_syntypes_piechart(dataset_stat),
                             className="six columns")],
                   className="row",
                   style={"margin-top": "50px",
                          "margin-left": "30px"}),
          html.Div(get_me_elements_freq_plot(materials_stat["elements_freq"]),
                   className="row"),
          html.Div(get_prec_anions_freq_plot(materials_stat["precursors_anion_freq"]),
                   className="row"),
          html.Div(get_temperature_per_syntype_plot(recipes_stat["temperature_per_syntype"]),
                   className="row")
          ]