import json


class PreProcessing:
    def open_settings(self):
        with open('./config/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset

    def open_ic_default(self):
        with open('./config/ic-preset/ic_settings.json', 'r') as json_file:
            iset = json.load(json_file)
        return iset