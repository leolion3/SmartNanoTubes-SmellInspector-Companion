#!/usr/bin/env python3
import random
from copy import deepcopy
from typing import List, Dict, Any, Tuple

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import config
from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter
from ml_adapters.ml_handler import ml_handler
from persistence.database_handler import database_handler as db


class ReTrainer:
    """
    Pre-trains all available ML models.
    """

    @staticmethod
    def _get_available_data() -> Tuple[List[str], List[List[float]]]:
        log.info(f'Reading training data from {config.DATABASE_FILE_PATH}', module=Module.PRE)
        data: List[Dict[str, Any]] = db.get_labelled_data()
        log.info('Total Data Entries:', len(data), module=Module.PRE)
        return [d['label'] + ' ' + d.get('quantity', '') for d in data], [d['data'] for d in data]

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
            _data, _labels, test_size=0.2, stratify=_labels, random_state=42
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

    def _re_train_models(self) -> None:
        old_model_data = deepcopy(self.classifiers)
        try:
            self.classifiers = self._train_models()
            log.info('Re-trained successfully.', module=Module.PRE)
        except Exception as e:
            log.error('Error re-training classifiers, reverting. Trace:', e, module=Module.PRE)
            self.classifiers = old_model_data

    def add_data(self, data: List[str], label: str, quantity: str) -> None:
        try:
            log.debug('Adding training data. Current count:', self._re_training_count, module=Module.PRE)
            db.add_data(data, label, quantity)
            self._re_training_count += 1
            if self._re_training_count >= config.RE_TRAINING_RATE:
                self._re_training_count = 0
                log.info('Reached re-training threshold, re-training models.')
                self._re_train_models()
        except Exception as e:
            log.error('Error adding training data. Trace:', e, module=Module.PRE)

    def persist_from_db_data(self, database: str) -> None:
        try:
            db.persist_from_db_data(database)
            log.info('Persisted successfully. Training models...', module=Module.PRE)
            self.classifiers = self._train_models()
            log.info('Models trained successfully.', module=Module.PRE)
        except Exception as e:
            log.error('Error persisting training data. Trace:', e, module=Module.PRE)

    def __init__(self):
        self.classifiers: Dict[str, MLAdapter] = {}
        self._re_training_count: int = 0


re_trainer: ReTrainer = ReTrainer()
