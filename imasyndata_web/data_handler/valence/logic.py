from imasyndata_web.constants import METAL_TYPES, VALENCE_PLOT_ROW_LEN
from imasyndata_web.data_handler.valence.components import serve_layout


def __get_compound_valences(composition):
    elements_valence = {}
    for compound in composition:
        for el, v in compound['valence'].items():
            if el not in elements_valence:
                elements_valence[el] = []
            elements_valence[el].append(v)

    return elements_valence


def __get_valence_tables(data):
    elements_target = {}
    elements_precursors = {}
    if all('_target' in row for row in data):
        for row in data:
            for el, valence in __get_compound_valences(row['_target']['composition']).items():
                if el not in elements_target:
                    elements_target[el] = []
                elements_target[el].extend(int(v) for v in valence if v > 0)
            for precursor in row['_precursors']:
                for el, valence in __get_compound_valences(precursor['composition']).items():
                    if el not in elements_precursors:
                        elements_precursors[el] = []
                    elements_precursors[el].extend(int(v) for v in valence if v > 0)

    return elements_target, elements_precursors


def build_valence_content(data):
    elements_target, elements_precursors = __get_valence_tables(data)

    if not elements_target or not elements_precursors:
        return []

    valence_layout = serve_layout(elements_target, elements_precursors)
    return valence_layout
