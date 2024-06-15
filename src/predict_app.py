import os
import  numpy as np
from flask import Flask, request, send_from_directory, url_for
from flask_cors import CORS

from dotenv import dotenv_values
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask import send_from_directory
from src.utils import predict_io_bounded, predict_cpu_bounded, predict_cpu_multithread

import pandas as pd
from joblib import load

MODEL_SAVE_PATH = 'models/lgbm.joblib'

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    config['APP_TOKEN']: "user1",
}

model = load(MODEL_SAVE_PATH)


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

def predict(in_data: dict) -> int:
    """ Predict house price from input data parameters.
    :param in_data: house parameters.
    :raise Error: If something goes wrong.
    :return: House price, RUB.
    :rtype: int
    """

    data = pd.DataFrame(in_data, index=[0])

    if 'county_short' not in data.columns:
        mapping = pd.read_csv('mapping/county.txt', sep='|')
        data = data.merge(mapping, left_on='district', right_on='district_name', how='left')
        data['county_short'] = np.where(data['county_short'].isna(), 'unknown', data['county_short'])
        data['county_short'] = np.where(data['county_short'] == 'Марьина роща', 'СВАО', data['county_short'])

    if 'object_type' not in data.columns:
        data['object_type'] = 'secondary'

    data[['total_meters', 'rooms_count', 'floor', 'floors_count']] = data[['total_meters', 'rooms_count', 'floor', 'floors_count']].astype(float)
    data['top_bottom_floor'] = np.where((data.floor == data.floors_count) | (data.floor == 1), 1, 0)
    data = pd.get_dummies(data, columns=['county_short'], dtype=int)

    need_cols = ['floor', 'floors_count', 'rooms_count', 'total_meters', 'top_bottom_floor', 'county_short_ВАО', 'county_short_ЗАО',
     'county_short_ЗелАО', 'county_short_САО', 'county_short_СВАО', 'county_short_СЗАО', 'county_short_ТАО',
     'county_short_ЦАО', 'county_short_ЮАО', 'county_short_ЮВАО', 'county_short_ЮЗАО', 'object_type_secondary']

    missing = list(set(need_cols) - set(data.columns))
    for i in missing:
        data[i] = 0

    data['object_type_secondary'] = np.where(data.object_type == 'secondary', 1, 0)
    data.drop(columns='object_type', inplace=True)

    data = data[need_cols]
    prediction = model.predict(data)

    upper = int(np.exp(prediction[0])) + 2_500_000
    lower = int(np.exp(prediction[0])) - 2_500_000

    return int(np.exp(prediction[0]))

@app.route("/")
def home():
    return '<h1>Housing price service.</h1> Use /predict endpoint'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')

@app.route("/predict", methods=['POST'])
def predict_web_serve():
    """Dummy service"""
    in_data = request.get_json()
    price = predict(in_data)
    return {'price': price}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
