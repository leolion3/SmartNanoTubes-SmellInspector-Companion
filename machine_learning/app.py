#!/usr/bin/env python3
from typing import Dict

import waitress
from flask import Flask, jsonify, request
from flask_cors import CORS

from ml_pretrainer import pre_trainer

app = Flask(__name__)
CORS(app)


def _get_route_dict(
        url: str,
        desc: str,
        method: str = 'GET',
        params: Dict[str, str] = None,
        body: Dict[str, str] = None,
        response: Dict[str, str] = None
) -> Dict[str, str | Dict[str, str]]:
    _dict = {
        'route': url,
        'method': method,
        'description': desc,
    }
    if params is not None:
        _dict['params'] = params
    if body is not None:
        _dict['body'] = body
    if response is not None:
        _dict['response'] = response
    return _dict


@app.route('/predict', methods=['POST'])
def predict():
    body = request.json
    if 'data' not in body:
        return jsonify({
            'error': 'No data provided.'
        }), 400
    data = body['data']
    if len(data) != 64:
        return jsonify({
            'error': 'Invalid data provided.'
        }), 400
    predictions = pre_trainer.predict([float(n) for n in data])
    return jsonify({
        'predictions': predictions
    }), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify([
        _get_route_dict('/', desc='shows this page'),
        _get_route_dict(
            '/predict',
            desc='Predicts the labels for a new data entry.',
            method='POST',
            body={
                'data': 'Sensor data as JSON array of 64 values.'
            },
            response={
                'status': '200',
                'predictions': [
                    {
                        'model_name': 'Name of the ML Model',
                        'predicted_label': 'Label predicted by the model.'
                    }
                ]
            })
    ])


if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=9090)
