import json

def settings():
    with open('./config/ic_settings.json', 'r') as json_file:
        iset = json.load(json_file)
    return iset