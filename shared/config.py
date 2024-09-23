import importlib.resources as impresources
import tomli


config_file = impresources.files(__name__) / 'config.toml'
with open(config_file, 'rb') as f:
    config = tomli.load(f)
