import json
from pymongo import MongoClient
from pprint import pprint

from imasyndata_web.constants import DB_COLLECTIONS, DB_STAT_PATH, MATERIALS_STAT_PATH, RECIPES_STAT_PATH
from imasyndata_web.utils import connect_to_db
from imasyndata_web.data_stats.analysis_tools import get_elements_freq, get_temperature_per_syntype, get_prec_ions_freq


def load_stat_data(filepath):
    if not filepath:
        print("Specify the path to the stat data")
        return []
    return json.loads(open(filepath).read())


def get_from_db(db_config_synpro, output_path):
    synpro = connect_to_db(db_config_synpro)

    db_stats = {}
    dois = set()
    for collection in DB_COLLECTIONS:
        db_stats[collection] = synpro[collection].count_documents({})
        print(collection, db_stats[collection])
        if "Recipe" in collection:
            for d in synpro[collection].find({}):
                dois.add(d["doi"])

    db_stats["doi"] = len(dois)

    if output_path:
        with open(output_path, "w") as f:
            f.write(json.dumps(db_stats))

    return db_stats


def get_materials_stat_from_db(db_config_synpro, output_path):
    synpro = connect_to_db(db_config_synpro)

    collection = [c for c in DB_COLLECTIONS if "Material" in c][0]
    materials_data = [d for d in synpro[collection].find({})]
    elements_freq = get_elements_freq(materials_data)
    precursors_anion_freq = get_prec_ions_freq(materials_data)

    output_data = dict(elements_freq=elements_freq,
                       precursors_anion_freq=precursors_anion_freq)

    if output_path:
        with open(output_path, "w") as f:
            f.write(json.dumps(output_data))

    return output_data


def get_recipes_stat_from_db(db_config_synpro, output_path):
    synpro = connect_to_db(db_config_synpro)
    collections = [c for c in DB_COLLECTIONS if "Recipe" in c]
    recipe_data = {t: [] for t in collections}
    for collection in collections:
        recipe_data[collection].extend(d for d in synpro[collection].find({}))

    temperature_per_syntype = get_temperature_per_syntype(recipe_data)

    output_data = dict(temperature_per_syntype=temperature_per_syntype)
    if output_path:
        with open(output_path, "w") as f:
            f.write(json.dumps(output_data))

    return output_data


# if __name__ == "__main__":
#     credentials = json.loads(open("credentials.json").read())
#     db_config_synpro = {"db_host": credentials["mongo_host"],
#                        "db_name": credentials["prod_db_name"],
#                        "db_login": credentials["prod_db_login"],
#                        "db_passwd": credentials["prod_db_passwd"]}
#
#     print("Calulating DB stat...")
#     db_stats = get_from_db(db_config_synpro, DB_STAT_PATH)
#
#     print("Calulating Materials stat...")
#     materials_stat = get_materials_stat_from_db(db_config_synpro, MATERIALS_STAT_PATH)
#
#     print("Calulating Recipes stat...")
#     recipes_stat = get_recipes_stat_from_db(db_config_synpro, RECIPES_STAT_PATH)