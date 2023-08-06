import pickle, os, json
from importlib_resources import files
from .models import DecompoundingModel

path = files('secos.models')
path = os.path.dirname(os.path.abspath(__file__))

def load(model_name):
    with open(path + f"/data/{model_name}.json", "r") as f:
        model = json.loads(f.read())
    return DecompoundingModel(**model)