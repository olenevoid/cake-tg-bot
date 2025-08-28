import json


def save_readable_json(dictionary, filepath):
    json_string = json.dumps(dictionary, indent=4, ensure_ascii=False)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json_string)


def load_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read()
        return json.loads(data)


def find_value_in_dict(pk, json_filepath):
    dictionary = load_from_json(json_filepath)
    return dictionary.get(str(pk))
