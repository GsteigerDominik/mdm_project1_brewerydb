import os
import pandas as pd
import pickle
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pathlib import Path

print("*** Init and load model ***")
directory_path = Path(".", "res/model/")
files = []
for filename in os.listdir(directory_path):
    files.append(filename)

print("*** Init Flask App ***")
app = Flask(__name__, static_url_path='/', static_folder='static')
cors = CORS(app)


@app.route("/")
def indexPage():
    return send_file("static/index.html")


@app.route("/api/model_versions")
def api_model_versions():
    return jsonify(files)


@app.route("/api/predict")
def api_predict():
    model = request.args.get('model', default="GradientBoostingRegressor.pkl")
    bitterness_ibu = request.args.get('bitterness_ibu', default=0, type=int)
    st_Cold = request.args.get('st_Cold', default=0, type=bool)
    bs_American_StyleImperialStout = request.args.get('bs_American_StyleImperialStout', default=0, type=bool)
    pfn_Bittersweet = request.args.get('pfn_Bittersweet', default=0, type=bool)
    color_srm = request.args.get('color_srm', default=0, type=int)

    with open(Path(".", "res/model/", model), 'rb') as fid:
        model = pickle.load(fid)

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
    app.run(host='0.0.0.0', debug=True)
