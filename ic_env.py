import json

def open_settings():
    with open('./config/ic_settings.json', 'r') as json_file:
        iset = json.load(json_file)
    return iset

def open_ic_default():
    with open('./config/ic-preset/ic_settings.json', 'r') as json_file:
        iset = json.load(json_file)
    return iset