import yaml
import json
#pip install pyyaml
with open('config.yaml', 'r') as file:
    configuration = yaml.safe_load(file)
with open('config1.json', 'w') as json_file:
    json.dump(configuration, json_file,indent=4)
with open('config1.json', 'r') as json_file:
    print(json_file.read())
