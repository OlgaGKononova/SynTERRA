import os
import requests

from imasyndata_web.utils import query_db
from imasyndata_web.constants import DEFAULT_TABLE_COLUMNS, EXT_COLUMNS_OPTIONS, MAP_COLLECTIONS
from imasyndata_web.search.components import syntypes_stats_plot
from imasyndata_web.operations_utils import reassign_operations, get_last_heating_step


def __get_variables_string(amounts_x):
    variables = []
    for var, value in amounts_x.items():
        if value['values']:
            var_string = var + " = " + ', '.join([str(v) for v in set(value['values'])])
        else:
            var_string = var
            if value['max_value']:
                var_string = var_string + ' < ' + str(value['max_value'])
            if value['min_value']:
                var_string = str(value['min_value']) + ' < ' + var_string
        variables.append(var_string)
    if variables:
        return "; ".join(variables)
    return ""


def __get_syntypes_table(data):
    syn_types = {}
    if all("synthesis_type" in row for row in data):
        for row in data:
            s_type = " ".join([s.capitalize() for s in row["synthesis_type"].split("_")[:-2]])
            if s_type not in syn_types:
                syn_types[s_type] = 0
            syn_types[s_type] += 1

    return syn_types


def get_recipes(input_text, collections, add_columns):
    """
    query output:
    _id, doi, synthesis_type, target, precursors, variables, reaction, reaction_string, targets_string
    """
    dataset, message = query_db(input_text, collections)

    table_output = []
    for data in dataset:

        if data["extraction"]:
            operations = reassign_operations(data["extraction"])
        else:
            operations = data["operations"]
        firing_step = get_last_heating_step(operations)
        if firing_step:
            operations[firing_step]["type"] = "FiringOperation"

        intro_text = [t["text"] for t in data.get("intro", [])
                      if t["path"] in {"_root", "_root$$Intro", "_root$$Introduction"} and t["order"] in {0, 1, 2}]

        operations_string = ' \u2192 '.join([op["type"] for op in operations])
        precursors_string = ", ".join([p['material_formula'] for p in data["precursors"]])
        variables_string = __get_variables_string(data["target"]["amounts_x"])


        table_output.append(dict(doi=data["doi"],
                                 synthesis_type=data["synthesis_type"],
                                 target=data["target"]["material_formula"],
                                 variables=variables_string,
                                 precursors=precursors_string,
                                 reaction=data["reaction_string"],
                                 operations=operations_string,

                                 _target=data["target"],
                                 _precursors=data["precursors"],
                                 _operations=operations,
                                 _intro_text = intro_text
                                 #_reaction=data["reaction"]
                                 ))

    output_columns = DEFAULT_TABLE_COLUMNS \
                     + [{"id": c, "name": c.replace("_", " ").capitalize()} for c in add_columns]

    syn_types_table = __get_syntypes_table(table_output)
    graph = ""
    if syn_types_table:
        graph = syntypes_stats_plot(syn_types_table)
    return table_output, output_columns, graph, message


def select_data(search_data, selected_row_indices):
    if not selected_row_indices:
        selected_row_indices = [i for i in range(len(search_data))]
    return [row for idx, row in enumerate(search_data) if idx in selected_row_indices]
