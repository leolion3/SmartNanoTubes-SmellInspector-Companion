#!/usr/bin/env python3
import uuid
from datetime import datetime
from typing import Dict, Any, List

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter
from ml_adapters.knn.knn_classifier import KNNClassifier
from ml_adapters.random_forest.random_forest_classifier import RandomForestClassifier
# from ml_adapters.xg_boost.xg_boost_classifier import XGBoostClassifier


class MLModelHandler:
    """
    Handles the available ML models
    """

    def get_instances(self) -> Dict[str, Any]:
        """
        Get a dictionary of ML model instances.
        :return:
        """
        return self._instances

    def create_instance(self, ml_model: str) -> Dict[str, Any]:
        """
        Creates a ML model instance.
        :param ml_model: the ML model type name.
        :return: the ML model instance data.
        """
        log.info(f"Creating ML model instance: {ml_model}", module=Module.ML)
        model_id: str = uuid.uuid1().hex
        _instance: MLAdapter = self._models[ml_model]()
        _mdict = {
            'type': ml_model,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'instance': _instance,
        }
        self._instances[model_id] = _mdict
        log.info(f"Created ML model instance: {ml_model} with id {model_id}", module=Module.ML)
        return {
            'id': model_id,
            'instance': _instance,
        }

    def get_available_models(self) -> List[str]:
        """
        Get a list of available ML models
        :return:
        """
        return list(self._models.keys())

    def __init__(self):
        """
        Default constructor.
        """
        log.info('Starting ML adapter...', module=Module.ML)
        self._models: Dict[str, Any] = {
            'KNN': KNNClassifier,
            'RF': RandomForestClassifier,
            # 'XGB': XGBoostClassifier,
        }
        self._instances = {}
        log.info('ML adapter started.', module=Module.ML)


ml_handler: MLModelHandler = MLModelHandler()
