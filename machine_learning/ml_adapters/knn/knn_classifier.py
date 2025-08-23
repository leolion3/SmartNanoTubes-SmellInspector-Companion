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
        log.info('Training KNN Classifier with downsampling...', module=Module.KNN)
        x = np.array(data)
        y = np.array(labels)

        air_mask = (y == "air")
        x_air, y_air = x[air_mask], y[air_mask]
        x_non_air, y_non_air = x[~air_mask], y[~air_mask]

        x_air_down, y_air_down = resample(
            x_air,
            y_air,
            replace=False,
            n_samples=len(y_non_air),
            random_state=42
        )
        x_balanced = np.vstack((x_air_down, x_non_air))
        y_balanced = np.concatenate((y_air_down, y_non_air))
        x_train, x_val, y_train, y_val = train_test_split(
            x_balanced, y_balanced, test_size=0.4, stratify=y_balanced, random_state=42
        )
        log.info('Scaling data...', module=Module.KNN)
        x_train_scaled = self._scaler.fit_transform(x_train)
        x_val_scaled = self._scaler.transform(x_val)
        log.info('Fitting model...', module=Module.KNN)
        self._knn.fit(x_train_scaled, y_train)
        accuracy = self._knn.score(x_val_scaled, y_val)
        log.info('Training done. Accuracy: %.3f' % accuracy, module=Module.KNN)

    @override
    def predict(self, data: List[List[float]]) -> List[str]:
        data_scaled = self._scaler.transform(data)
        return self._knn.predict(data_scaled)

    def __init__(self, k: int = 7):
        """
        Default constructor.
        :param k: the amount of neighbors.
        """
        self._knn = KNeighborsClassifier(n_neighbors=k)
        self._scaler: StandardScaler = StandardScaler()
