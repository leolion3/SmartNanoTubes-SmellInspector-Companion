#!/usr/bin/env python3
import random
from typing import List, Dict, Any, Tuple

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import config
from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter
from ml_adapters.ml_handler import ml_handler
from persistence.database_handler import DatabaseHandler


class PreTrainer:
    """
    Pre-trains all available ML models.
    """

    @staticmethod
    def _get_available_data() -> Tuple[List[str], List[List[float]]]:
        log.info(f'Reading training data from {config.DATABASE_FILE_PATH}', module=Module.PRE)
        db: DatabaseHandler = DatabaseHandler(db_path=config.DATABASE_FILE_PATH)
        experiments: List[str] = db.get_experiment_list()
        log.info('Available experiments:', experiments, module=Module.PRE)
        log.info('Available substances:', db.get_substances(), module=Module.PRE)
        data: List[Dict[str, Any]] = db.get_labelled_data(experiments[0])
        log.info('Total Data Entries:', len(data), module=Module.PRE)
        return [d['label'] for d in data], [d['data'] for d in data]

    @staticmethod
    def _train_model(data: List[List[float]], labels: List[str], model_idx: int) -> MLAdapter:
        model_id: str = ml_handler.get_available_models()[model_idx]
        model: Dict[str, any] = ml_handler.create_instance(model_id)
        classifier: MLAdapter = model['instance']
        classifier.fit(data, labels)
        return classifier

    @staticmethod
    def _predict_random(model: MLAdapter, data: List[List[float]], labels: List[str]) -> None:
        random_idx: int = random.randint(0, len(data) - 1)
        predicted_label: List[str] = model.predict([data[random_idx]])
        log.info('Predicted label:', predicted_label[0], 'actual:', labels[random_idx], module=Module.PRE)

    def predict(self, data: List[float]) -> Dict[str, str]:
        """
        Makes label predictions for the given data point using all available ML adapters.
        :param data: the data from the sensor - an array of 64 values.
        :return: the predicted labels as a dict of model name to predicted label.
        """
        results: Dict[str, str] = {}
        for model_name, classifier in self.classifiers.items():
            try:
                results[model_name] = classifier.predict([data])[0]
                log.debug(f'Model: {model_name}, predicted label: {results[model_name]}', module=Module.PRE)
            except Exception as e:
                log.error(f'Error trying to predict label with model {model_name}. Trace:', e, module=Module.PRE)
        return results

    def _train_models(self) -> Dict[str, MLAdapter]:
        """
        Trains all available ML models and returns them as a dict of names to MLAdapter objects.
        :return: the dictionary of names to MLAdapter objects.
        """
        _labels, _data = self._get_available_data()
        x_train, x_test, y_train, y_test = train_test_split(
            _data, _labels, test_size=0.05, stratify=_labels, random_state=42
        )
        classifiers: Dict[str, MLAdapter] = {}
        for i, model_name in enumerate(ml_handler.get_available_models()):
            try:
                log.info(f'Training {model_name} classifier...', module=Module.PRE)
                _classifier = self._train_model(x_train, y_train, i)
                y_pred = _classifier.predict(x_test)
                report = classification_report(y_test, y_pred, digits=3)
                log.info(f"=== {model_name} Classification Report ===", module=Module.PRE)
                log.info(report, module=Module.PRE)
                classifiers[model_name] = _classifier
            except Exception as e:
                log.error(f'Error training {model_name} classifier. Trace:', e, module=Module.PRE)
        return classifiers

    def __init__(self):
        log.info('Starting ML Pre-Trainer...', module=Module.PRE)
        self.classifiers: Dict[str, MLAdapter] = self._train_models()
        log.info('Pre-Trainer ready.', module=Module.PRE)


pre_trainer: PreTrainer = PreTrainer()
