from .models import DecompoundingModel
import requests, shutil, zipfile, os, pickle
from tqdm import tqdm

# Extract the file name from the URL
MODEL_URL = 'https://secos-model-data.s3.eu-west-2.amazonaws.com/'

def download(model_name, overwrite=False):
    script_dir = os.path.dirname(os.path.abspath(__file__)) + '/data/'
    os.makedirs(script_dir, exist_ok=True)

    if all([overwrite==False, model_name + ".json" in os.listdir(script_dir)]):
        raise Exception("Model already download. To overwrite, set overwrite=True")
    
    # Download the zip file
    response = requests.get(MODEL_URL + model_name + '.json', stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
    with open(script_dir + model_name + '.json', "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                # Write the chunk to the file
                file.write(chunk)
                # Update the progress bar with the chunk size
                progress_bar.update(len(chunk))

    # Close the progress bar
    progress_bar.close()

    print("Download completed!")