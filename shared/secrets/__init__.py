import importlib.resources as impresources
import subprocess
import yaml
from yaml import Loader


secrets_file = impresources.files(__name__) / 'secrets.yaml'
decrypt_secrets = subprocess.run(["sops", "decrypt", secrets_file], stdout=subprocess.PIPE)
decrypt_secrets.check_returncode()
secrets = yaml.load(decrypt_secrets.stdout, Loader=Loader)
