import yaml

# TODO: The config.yaml should only be load once, maybe we should pack it as a class (?)

def get(key):
    with open("config.yaml", "r") as f:
        data = yaml.load(f)
    try:
        return data[key]
    except:
        raise


