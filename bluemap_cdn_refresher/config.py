import ruamel.yaml

with open("config.yaml", "r") as f:
    config = ruamel.yaml.safe_load(f)
