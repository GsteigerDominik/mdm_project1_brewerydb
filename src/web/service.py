# python -m flask --debug --app service run (works also in PowerShell)

import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlobServiceClient
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# init app, load model from storage
print("*** Init and load model ***")
if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("hikeplanner-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("hikeplanner-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("../../res/model/").mkdir(parents=True, exist_ok=True)
    download_file_path = os.path.join("../model", "GradientBoostingRegressor.pkl")
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.environ)
    print("AZURE_STORAGE_CONNECTION_STRING not set")

file_path = Path(".", "res/model/", "GradientBoostingRegressor.pkl")
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)

print("*** Init Flask App ***")
app = Flask(__name__,static_url_path='/', static_folder='static')
cors = CORS(app)


@app.route("/")
def indexPage():
    return send_file("static/index.html")


@app.route("/api/predict")
def api_predict():
    bitterness_ibu = request.args.get('bitterness_ibu', default=0, type=int)
    st_Cold = request.args.get('st_Cold', default=0, type=bool)
    bs_American_StyleImperialStout = request.args.get('bs_American_StyleImperialStout', default=0, type=bool)
    pfn_Bittersweet = request.args.get('pfn_Bittersweet', default=0, type=bool)
    color_srm = request.args.get('color_srm', default=0, type=int)

    demoinput = [[bitterness_ibu, st_Cold, bs_American_StyleImperialStout, pfn_Bittersweet, color_srm]]
    demodf = pd.DataFrame(
        columns=['bitterness_ibu', 'st_Cold', 'bs_American-StyleImperialStout', 'pfn_Bittersweet', 'color_srm'],
        data=demoinput)
    demooutput = model.predict(demodf)
    abv = demooutput[0]

    return jsonify({
        'abv': str(abv)
    })

if __name__ == '__main__':
    # host='0.0.0.0' damit lokaler Zugriff auf Port 5000 funktioniert
    app.run(host='0.0.0.0', debug=True)