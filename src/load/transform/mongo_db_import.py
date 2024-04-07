import argparse
import json
import os
from pymongo import MongoClient

from parser import *


def cleanup(obj):
    for key, value in obj.items():
        if isinstance(value, list):
            obj[key] = [item for item in obj[key] if item != ""]
        elif isinstance(value, str):
            if not value.strip():
                obj[key] = None
    obj = {key: value for key, value in obj.items() if value is not []}
    obj = {key: value for key, value in obj.items() if value is not None}
    return obj


def to_object(item):
    try:
        obj = {
            "url": item['url'],
            "alcohol_by_volume": parse_abv(item["abv"]),
            "brew_style": parse_brew_style(item["brew_style"]),
            "primary_flavor_notes": parse_primary_flavor_notes(item["primary_flavor_notes"]),
            "color_srm": parse_srm(item["srm"]),
            "bitterness_ibu": parse_ibu(item["ibu"]),
            "serving_temperature": parse_serving_temperature(item["serving_temperature"])
        }
        return cleanup(obj)

    except Exception as e:
        print("Could not read {}".format(item["files"][0]), e)
        return None


class JsonLinesImporter:

    def __init__(self, file, mongo_uri, batch_size=30, db='mdmBreweryDb', collection='beer'):
        self.file = file
        self.base_dir = os.path.dirname(file)
        self.batch_size = batch_size
        self.client = MongoClient(mongo_uri)
        self.db = db
        self.collection = collection

    def read_lines(self):
        with open(self.file, encoding='UTF-8') as f:
            data = f.read().strip()
            json_list = json.loads(data)
            for item in json_list:
                yield to_object(item)

    def save_to_mongodb(self):
        db = self.client[self.db]
        collection = db[self.collection]
        for data in self.read_lines():
            pipeline = [{"$match": {"url": data['url']}}]
            results = collection.aggregate(pipeline)
            if next(results, None) is not None:
                print("Document already exists:", data['url'])
            else:
                print("inserting document", data)
                collection.insert_one(data)

    def save_to_file(self):
        with open("beer.json", "w") as file:
            for data in self.read_lines():
                json.dump(data, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
    parser.add_argument('-i', '--input', required=True, help="input file in JSON Lines format")
    parser.add_argument('-c', '--collection', required=True,
                        help="name of the mongodb collection where the tracks should be stored")
    args = parser.parse_args()
    importer = JsonLinesImporter(args.input, collection=args.collection, mongo_uri=args.uri)
    importer.save_to_mongodb()
