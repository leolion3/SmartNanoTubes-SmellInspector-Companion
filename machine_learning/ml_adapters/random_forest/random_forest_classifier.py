#!/usr/bin/env python3
from typing import override, List

from sklearn.ensemble import RandomForestClassifier as SkRandomForest
from sklearn.preprocessing import StandardScaler

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter


class RandomForestClassifier(MLAdapter):
    """
    Implements a random forest classifier with two-step classification:
    1. Detect if the sample is 'air'.
    2. If not, classify between 'domol' and 'octeniderm'.
    """

    def __init__(self, n_estimators: int = 200):
        """
        Default constructor.
        :param n_estimators: Number of trees in the random forest.
        """
        self._scaler: StandardScaler = StandardScaler()
        self._clf_substance = SkRandomForest(n_estimators=n_estimators, random_state=42)

    @override
    def fit(self, data: List[List[float]], labels: List[str]) -> None:
        """
        Train the random forest classifier.
        :param data: the training data.
        :param labels: the training labels.
        :return:
        """
        log.info('Training Random Forest Classifier...', module=Module.RF)
        log.info('Scaling data...', module=Module.RF)
        x_scaled = self._scaler.fit_transform(data)
        log.info('Fitting air detector...', module=Module.RF)
        log.info('Fitting substance classifier...', module=Module.RF)
        self._clf_substance.fit(x_scaled, labels)

    @property
    def classes_(self) -> List[str]:
        if hasattr(self._clf_substance, "classes_"):
            return list(self._clf_substance.classes_)
        return []

    @override
    def predict(self, data: List[List[float]]) -> List[str]:
        """
        Predict labels for given samples.
        :param data: input data.
        :return: predicted labels.
        """
        x_scaled = self._scaler.transform(data)
        return self._clf_substance.predict(x_scaled)
