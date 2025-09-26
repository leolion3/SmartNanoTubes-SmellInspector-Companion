#!/usr/bin/env python3
from typing import override, List

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter
import numpy as np
from sklearn.utils import resample


class KNNClassifier(MLAdapter):
    """
    Implements a simple k-nearest neighbors classifier.
    """

    @override
    def fit(self, data: List[List[float]], labels: List[str]) -> None:
        """
        Train the KNN classifier.
        :param data: the training data.
        :param labels: the training labels.
        :return:
        """
        log.info('Training KNN Classifier...', module=Module.KNN)
        log.info('Scaling data...', module=Module.KNN)
        x_scaled = self._scaler.fit_transform(data)
        log.info('Fitting model...', module=Module.KNN)
        self._knn.fit(x_scaled, labels)

    @override
    def predict(self, data: List[List[float]]) -> List[str]:
        data_scaled = self._scaler.transform(data)
        return self._knn.predict(data_scaled)

    @property
    def classes_(self) -> List[str]:
        if hasattr(self._knn, "classes_"):
            return list(self._knn.classes_)
        return []

    def __init__(self, k: int = 7):
        """
        Default constructor.
        :param k: the amount of neighbors.
        """
        self._knn = KNeighborsClassifier(n_neighbors=k)
        self._scaler: StandardScaler = StandardScaler()
