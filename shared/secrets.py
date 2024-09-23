import importlib.resources as impresources
import tomli


secrets_file = impresources.files(__name__) / 'secrets.toml'
with open(secrets_file, 'rb') as f:
    secrets = tomli.load(f)
