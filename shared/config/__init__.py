import importlib.resources as impresources
import yaml
from yaml import Loader


config_file = impresources.files(__name__) / 'config.yaml'
with open(config_file, 'rb') as f:
    config = yaml.load(f, Loader=Loader)
