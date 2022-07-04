import json
from pymongo import MongoClient

from imasyndata_web.utils import connect_to_db
from imasyndata_web.constants import PUB_STAT_PATH, SYN_TYPES

from pprint import pprint


def load_from_file(filepath="imasyndata/static/publishers_stats.json"):
    return json.loads(open(filepath).read())


def __get_papers_stat(db_config):
    full_text_db = connect_to_db(db_config)

    # total number of papers
    nr_of_papers = full_text_db.Paper_Raw_HTML.count_documents({})

    # Total publishers
    available_publishers = []
    publishers = full_text_db.Paper_Metadata.aggregate([{"$group": {"_id": "$Publisher",
                                                                    "count": {"$sum": 1}}},
                                                        {"$sort": {"count": -1}}])
    while publishers.alive:
        p = publishers.next()
        available_publishers.append((p["_id"], p["count"]))

    publishers_data = {p: {"nr_of_HTML": c,
                           "nr_of_parsed": 0,
                           "nr_of_paragraphs": 0,
                           "syn_types_count": {t: 0 for t in SYN_TYPES}} for p, c in available_publishers}

    # scraped papers per publisher
    for publisher, c in available_publishers:
        publishers_data[publisher]["nr_of_parsed"] = \
            full_text_db.Paper_Parsed.count_documents({"$and": [{"parser_version": {"$regex": publisher + "*"}},
                                                                {"parser_successful": True}]})

    return nr_of_papers, publishers_data


def get_from_db(db_config_text, db_config_synpro, output_path):
    _, publishers_data = __get_papers_stat(db_config_text)
    available_publishers = {p for p in publishers_data.keys()}

    synpro = connect_to_db(db_config_synpro)
    # recipe paragraphs per publisher
    for publisher in available_publishers:
        publishers_data[publisher]["nr_of_paragraphs"] = synpro.Paragraphs.count_documents({"Publisher": publisher})
        for syn_type in SYN_TYPES:
            publishers_data[publisher]["syn_types_count"][syn_type] = \
                synpro.Paragraphs_Meta.aggregate([{"$lookup": {"from": "Paragraphs",
                                                               "localField": "paragraph_id",
                                                               "foreignField": "_id",
                                                               "as": "meta"}},
                                                  {"$unwind": "$meta"},
                                                  {"$project": {"classification": 1,
                                                                "DOI": 1,
                                                                "meta.Publisher": 1,
                                                                "confidence": 1,
                                                                "paragraph_text": 1}},
                                                  {"$match": {"classification": syn_type,
                                                              "meta.Publisher": publisher,
                                                              "confidence": {"$gt": 0.3}}},
                                                  {"$count": "amount"},
                                                  {"$sort": {"confidence": -1}}]).next()["amount"]

    if output_path:
        with open(output_path, "w") as f:
            f.write(json.dumps(publishers_data))

    return publishers_data


def get_publisher_data(filepath=PUB_STAT_PATH):
    if filepath:
        return load_from_file(filepath)
    return get_from_db()


def get_publishers():
    publishers_data = get_publisher_data()
    return set(p for p in publishers_data.keys())


def get_recipes_stat(publisher):
    publishers_data = get_publisher_data()
    if publisher:
        return publishers_data[publisher]

    nr_of_HTML = 0
    nr_of_parsed = 0
    syn_types_count = {}
    for _, d in publishers_data.items():
        nr_of_HTML += d["nr_of_HTML"]
        nr_of_parsed += d["nr_of_parsed"]
        for t, count in d["syn_types_count"].items():
            if t not in syn_types_count:
                syn_types_count[t] = 0
            syn_types_count[t] += count
    return {"nr_of_HTML": nr_of_HTML,
            "nr_of_parsed": nr_of_parsed,
            "syn_types_count": syn_types_count}


def publisher2acronym():
    publishers = get_publishers()
    mapping = {}
    for p in publishers:
        if len(p.split(" ")) == 1:
            mapping[p] = p
        else:
            acron = "".join([t[0] for t in p.split(" ") if t not in ["The", "of"]])
            mapping[p] = acron
    return mapping


def acronym2publisher():
    publishers = get_publishers()
    mapping = {}
    for p in publishers:
        if len(p.split(" ")) == 1:
            mapping[p] = p
        else:
            acron = "".join([t[0] for t in p.split(" ") if t not in ["The", "of"]])
            mapping[acron] = p
    return mapping


# if __name__ == "__main__":
#     credentials = json.loads(open("credentials.json").read())
#     db_config_text = {"db_host": credentials["mongo_host"],
#                       "db_name": credentials["text_db_name"],
#                       "db_login": credentials["text_db_login"],
#                       "db_passwd": credentials["text_db_passwd"]
#                       }
#     db_config_synpro = {"db_host": credentials["mongo_host"],
#                           "db_name": credentials["prod_db_name"],
#                           "db_login": credentials["prod_db_login"],
#                           "db_passwd": credentials["prod_db_passwd"]
#                           }
#     publishers_data = get_from_db(db_config_text, db_config_synpro, "static/publishers_stats.json")
#
#     pprint(publishers_data)




