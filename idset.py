

import json5

# json 파일을 읽어서 설정값을 반환한다.
def load_settings():
    with open('./config/idsettings.jsonc', 'r') as jsonc_file:
        settings = json5.load(jsonc_file)
    return settings