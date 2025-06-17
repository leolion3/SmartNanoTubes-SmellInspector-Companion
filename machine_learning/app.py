#!/usr/bin/env python3
import os
import random
from typing import List, Dict, Any, Tuple

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter
from persistence.database_handler import DatabaseHandler
from ml_adapters.ml_handler import ml_handler
import setup


def get_available_data() -> Tuple[List[str], List[List[float]]]:
    fp: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), setup.DATA_DIR, 'database.db')
    db: DatabaseHandler = DatabaseHandler(db_path=fp)
    experiments: List[str] = db.get_experiment_list()
    log.info('Available experiments:', experiments, module=Module.MAIN)
    log.info('Available substances:', db.get_substances(), module=Module.MAIN)
    data: List[Dict[str, Any]] = db.get_labelled_data(experiments[0])
    log.info('Total Data Entries:', len(data), module=Module.MAIN)
    return [d['label'] for d in data], [d['data'] for d in data]


def train_model(data: List[List[float]], labels: List[str]) -> MLAdapter:
    knn_id: str = ml_handler.get_available_models()[0]
    model: Dict[str, any] = ml_handler.create_instance(knn_id)
    classifier: MLAdapter = model['instance']
    classifier.fit(data, labels)
    return classifier


def predict_random(model: MLAdapter, data: List[List[float]], labels: List[str]) -> None:
    random_idx: int = random.randint(0, len(data) - 1)
    predicted_label: List[str] = model.predict([data[random_idx]])
    log.info('Predicted label:', predicted_label, 'actual:', labels[random_idx], module=Module.MAIN)


if __name__ == '__main__':
    _labels, _data = get_available_data()
    _classifier = train_model(_data, _labels)
    for i in range(100):
        predict_random(_classifier, _data, _labels)
