import importlib.resources as impresources
import tomllib


secrets_file = impresources.files(__name__) / 'secrets.toml'
with open(secrets_file, 'rb') as f:
    secrets = tomllib.load(f)
