import json


def parse(input_file):
    raw = json.load(input_file)
    url_dict = {}
    for key, recipe_data in raw.iteritems():
        url_dict[key] = recipe_data['mainImage']
    return url_dict
