#!/usr/bin/env python3
from typing import Dict, Optional, Any

import sys
import waitress
from flask import Flask, jsonify, request
from flask_cors import CORS
from logging_framework.log_handler import log as logger, Module

import config
from ml_retrainer import re_trainer

app = Flask(__name__)
CORS(app, origins=['*'])


def _get_route_dict(
        url: str,
        desc: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        response: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    _dict: Dict[str, Any] = {
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
    predictions = re_trainer.predict([float(n) for n in data])
    return jsonify({
        'predictions': predictions
    }), 200


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        'status': 'ok'
    }), 200


@app.route('/new', methods=['POST'])
def persist_new_data():
    try:
        data = request.json
        if 'data' not in data or data['data'] == []:
            return jsonify({
                'error': 'No data provided.'
            }), 200
        re_trainer.add_data(
            data['data'],
            data['substance'],
            data['quantity']
        )
        return jsonify({
            'status': 'ok'
        }), 200
    except Exception as e:
        # Send 200 to kill companion thread.
        return jsonify({
            'error': str(e)
        }), 200


@app.route('/initial-data', methods=['POST'])
def persist_initial_data():
    try:
        database = request.json['data']
        if database is None or database == []:
            return jsonify({
                'error': 'No data provided.'
            }), 200
        re_trainer.persist_from_db_data(database)
        return jsonify({
            'status': 'ok'
        }), 200
    except Exception as e:
        # Send 200 to kill companion thread.
        return jsonify({
            'error': str(e)
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
    if '-m' in sys.argv:
        logger.info('Running in standalone mode.', module=Module.MAIN)
        config.STANDALONE_EXEC = True
    waitress.serve(app, host='0.0.0.0', port=9090)
