#!/usr/bin/env python3
from typing import override, List

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter


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
        x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.4, stratify=labels)
        x_train_scaled = self._scaler.fit_transform(x_train)
        x_val_scaled = self._scaler.transform(x_val)
        log.info('Fitting model...', module=Module.KNN)
        self._knn.fit(x_train_scaled, y_train)
        accuracy = self._knn.score(x_val_scaled, y_val)
        log.info('Training done. Accuracy:', accuracy, module=Module.KNN)

    @override
    def predict(self, data: List[List[float]]) -> List[str]:
        return self._knn.predict(data)

    def __init__(self, k: int = 7):
        """
        Default constructor.
        :param k: the amount of neighbors.
        """
        self._knn = KNeighborsClassifier(n_neighbors=k)
        self._scaler: StandardScaler = StandardScaler()
