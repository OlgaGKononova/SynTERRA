import json
from pymongo import MongoClient
from bson import ObjectId

from imasyndata_web.data_handler.wordcloud.components import generate_image


def build_application_content(data_table):
    return generate_image([t for data in data_table for t in data["_intro_text"]])