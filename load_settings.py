import json5

# Getting jsonc file and returning values.
def from_jsonc():
    with open('./config/idsettings.jsonc', 'r') as jsonc_file:
        idset = json5.load(jsonc_file)
    return idset