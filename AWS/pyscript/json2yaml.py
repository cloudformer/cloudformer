import yaml
import json
#pip install pyyaml
with open('vpc-2.json', 'r') as file:
    configuration = json.load(file)
with open('../YAML/1_EC2/vpc-2.yaml', 'w') as yaml_file:
    yaml.dump(configuration, yaml_file)
with open('../YAML/1_EC2/vpc-2.yaml', 'r') as yaml_file:
    print(yaml_file.read())