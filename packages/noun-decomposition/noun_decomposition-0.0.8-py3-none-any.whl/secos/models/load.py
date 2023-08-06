import pickle, os, json
from importlib_resources import files
from .models import DecompoundingModel

path = files('secos.models')
path = os.path.dirname(os.path.abspath(__file__))

def load(model_name):
    try:
        with open(path + f"/data/{model_name}.json", "r") as f:
            model = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Model {model_name} not found. Use secos.models.download('{model_name}') to download the model.")
    return DecompoundingModel(**model)