import os
import time
import requests
import pandas as pd
import regex as re

from scipy.stats import iqr
from flask import request
from pymongo import MongoClient

from imasyndata_web.constants import HTML_ENCODING, MAP_COLLECTIONS, DOWNLOAD_FOLDER, MATQUERY


def connect_to_db(config):
    mc = MongoClient(config["db_host"])
    db = mc[config["db_name"]]
    db.authenticate(config["db_login"], config["db_passwd"])
    return db


def __generate_query(input_text, collections):
    query_line = "?queryline=" + input_text

    for c, r in HTML_ENCODING.items():
        query_line = query_line.replace(c, r)

    for collection in collections:
        query_line += "&collections=" + MAP_COLLECTIONS.get(collection, collection)

    return query_line


def query_db(input_text, collections):

    search_keyword = re.match("^\$([a-z]+)\.", input_text).group(1) + "/"
    queryline = __generate_query(input_text, collections)
    #query_arg = MATQUERY + search_keyword + queryline
    query_arg = os.path.join(MATQUERY, search_keyword, queryline)
    result = requests.get(query_arg).json()

    if result["error"]:
        return [], result["message"]

    return result["results"], ""


def generate_download_link(data):
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), DOWNLOAD_FOLDER)
    filename = "search_results_" + str(time.time()) + ".csv"
    file_path = os.path.join(dir_path, filename)
    pd.DataFrame(data).to_csv(file_path)
    url_name = request.url_root
    output = url_name + file_path
    link_label = "Download Data"
    return link_label, output, filename


def get_material_elements(material):
    return list(set(el for c in material["composition"] for el in c["elements"].keys()))


def get_bins_number(arr):
    bin_width = iqr(arr) * 2.0 / (len(arr)) ** (1 / 3)
    interval = max(arr) - min(arr)
    if bin_width * interval == 0.0:
        return 1
    return int(interval / bin_width)