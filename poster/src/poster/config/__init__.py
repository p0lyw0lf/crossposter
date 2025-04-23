import importlib.resources as impresources
import yaml
from yaml import Loader


config_file = impresources.files(__name__) / 'config.yaml'
with config_file.open('rb') as f:
    config = yaml.load(f, Loader=Loader)
