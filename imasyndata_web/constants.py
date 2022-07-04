import os

PUB_STAT_PATH = "imasyndata_web/static/publishers_stats.json"
DB_STAT_PATH = "imasyndata_web/static/database_stats.json"
MATERIALS_STAT_PATH = "imasyndata_web/static/materials_stats.json"
RECIPES_STAT_PATH = "imasyndata_web/static/recipes_stats.json"

MATQUERY = os.environ.get("MATQUERY_API", "")
#MATQUERY = "http://lb.imasyndata.production.svc.spin.nersc.org/matquery/"
#MATQUERY = "http://landau.lbl.gov:8052/matquery/"

SYN_TYPES = {'hydrothermal_ceramic_synthesis',
             'precipitation_ceramic_synthesis',
             'sol_gel_ceramic_synthesis',
             'solid_state_ceramic_synthesis'}

DB_COLLECTIONS = {"Reactions_Data_v20",
                  "Materials_Data_v20",
                  "Recipes_Solid_State_v20",
                  "Recipes_Sol_Gel_v20",
                  "Recipes_Precipitation_v20",
                  "Recipes_Hydrothermal_v20"
                  }

SYN_TYPES2COLLECTIONS = {'hydrothermal_ceramic_synthesis': "Recipes_Hydrothermal_v20",
                         'precipitation_ceramic_synthesis': "Recipes_Precipitation_v20",
                         'sol_gel_ceramic_synthesis': "Recipes_Sol_Gel_v20",
                         'solid_state_ceramic_synthesis': "Recipes_Solid_State_v20"}

VALENCE_LBL_TITLE = "Distribution of oxidation states in target (red) and precursors (green) cations."
INPUT_PLACEHOLDER = "e.g. $target.allElem: {Li, Co, Mn} && $precursors.formula: {Li2CO3, Co3O4}"

# DEFAULT_TABLE_COLUMNS = [["DOI", ""],
#                          ["Materials", "Targets"],
#                          ["Materials", "Precursors"],
#                          ["Materials", "Variables"]]

DEFAULT_TABLE_COLUMNS = [{'id': 'doi', 'name': "DOI"},
                         {'id': 'target', 'name': "Targets"},
                         {'id': 'precursors', 'name': "Precursors"},
                         {'id': 'variables', 'name': "Variables"}]

TABLE_COLUMNS_WIDTH = [{'if': {'column_id': 'doi'},
                        'width': '70px'},
                       {'if': {'column_id': 'target'},
                        'width': '70px'},
                       {'if': {'column_id': 'precursors'},
                        'width': '120px'},
                       {'if': {'column_id': 'variables'},
                        'width': '70px'},
                       {'if': {'column_id': 'synthesis_type'},
                        'width': '70px'},
                       {'if': {'column_id': 'reaction'},
                        'width': '150px'},
                       {'if': {'column_id': 'operations'},
                        'width': '100px'},
                       ]

COLLECTIONS_OPTIONS = [{'label': 'solid-state', 'value': 'SSR'},
                       {'label': 'sol-gel', 'value': 'SGR'},
                       {'label': 'hydrothermal', 'value': 'HTR'},
                       {'label': 'precipitation', 'value': 'PPR'}]

MAP_COLLECTIONS = {"SSR": "Recipes_Solid_State_v20",
                   "SGR": "Recipes_Sol_Gel_v20",
                   "PPR": "Recipes_Precipitation_v20",
                   "HTR": "Recipes_Hydrothermal_v20"
                   }

EXT_COLUMNS_OPTIONS = [{'label': 'Synthesis type', 'value': 'synthesis_type'},
                       {'label': 'Reaction', 'value': 'reaction'},
                       {'label': 'Operations', 'value': 'operations'},
                       #{'label': 'Temperature range', 'value': 'temp_range'},
                       #{'label': 'Atmosphere', 'value': 'atmosphere'}
                       ]

HTML_ENCODING = {" ": "%20",
                 "$": "%24",
                 "&&": "%26%26",
                 ":": "%3A",
                 "{": "%7B",
                 "}": "%7D",
                 ".": "%2E",
                 "_": "%5F"}

DOWNLOAD_FOLDER = "downloads/"

METAL_TYPES = {#"non_metals": ['H', 'C', 'N', 'O', 'F', 'Cl', 'S', 'P', 'Se', 'Br', 'I'],
               "alkali_me": ['Li', 'Na', 'K', 'Rb', 'Cs'],
               "alkaline_me": ['Be', 'Ca', 'Sr', 'Ba'],
               "transition_me_4": ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn'],
               "transition_me_5": ['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd'],
               "transition_me_6": ['Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg'],
               "lanthanoid": ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Yb', 'Lu'],
               "other_me": ['B', 'Al', 'Ga', 'In', 'Tl', 'Si', 'Ge', 'Sn', 'Pb', 'As', 'Sb', 'Bi', 'Te'],
               }

VALENCE_PLOT_ROW_LEN = 10

IMAGES_LOCATION = 'http://ceder.berkeley.edu/filesstoring/'

"""
operations reassignment
"""
_MIXING_TERMS_PATH = '/home/olga/PycharmProjects/CederGroup_IMaSynProject/IMaSynData/imasyndata_web/static/aqueous_terms'
MIXING_ENV = [line.strip("\n") for line in open(_MIXING_TERMS_PATH, 'r')]
SOLUTION_VERBS = ["dissolv", "drop", "dilute"]
DISPERSION_VERBS = ['dispers', 'pulveriz', 'pulveris', 'suspend', 'spray', 'moisten', 'stir']
MILLING_TERMS = ["ballmill", "mill", "ball-mill"]


"""
data analysis of collections
"""
ELEMENTS_1 = ['H', 'B', 'C', 'N', 'O', 'F', 'P', 'S', 'K', 'V', 'Y', 'I', 'W', 'U']
ELEMENTS_2 = ['He', 'Li', 'Be', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'Cl', 'Ar', 'Ca', 'Sc', 'Ti', 'Cr',
              'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr',
              'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'Xe',
              'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
              'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
              'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf',
              'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',
              'Fl', 'Lv']
ELEMENTS = ELEMENTS_1 + ELEMENTS_2