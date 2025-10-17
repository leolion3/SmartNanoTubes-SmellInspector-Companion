#!/usr/bin/env python3
from typing import override, List

import numpy as np
from sklearn.ensemble import RandomForestClassifier as SkRandomForest
from sklearn.preprocessing import StandardScaler, RobustScaler

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter


class RandomForestClassifier(MLAdapter):
    """
    Implements a random forest classifier with two-step classification:
    1. Detect if the sample is 'air'.
    2. If not, classify between 'domol' and 'octeniderm'.
    """

    def __init__(self, n_estimators: int = 100):
        """
        Default constructor.
        :param n_estimators: Number of trees in the random forest.
        """
        self._scaler: StandardScaler = StandardScaler()
        # self._scaler: RobustScaler = RobustScaler()
        self._initial_n_estimators = n_estimators
        self._clf_substance = SkRandomForest(
            n_estimators=n_estimators,
            random_state=42,
            oob_score=True,
            n_jobs=-1,
            warm_start=True
        )

    def _auto_select_n_estimators(self, x_scaled: np.ndarray, y: List[str]) -> int:
        """
        Automatically select the number of trees based on OOB score curve.
        """
        log.info("Auto-selecting optimal n_estimators...", module=Module.RF)
        step_sizes = [10, 20, 50, 100, 200, 300, 500, 700, 1000]
        best_n = self._initial_n_estimators
        best_score = -np.inf
        for n in step_sizes:
            self._clf_substance.n_estimators = n
            self._clf_substance.fit(x_scaled, y)
            score = self._clf_substance.oob_score_
            log.info(f"OOB score with {n} trees: {score:.4f}", module=Module.RF)
            if score > best_score + 1e-4:  # small tolerance to avoid overfitting to noise
                best_score = score
                best_n = n
            # Optional: early stopping if improvement is marginal
            if n > 50 and (best_score - score) > 0.001:
                break
        log.info(f"Selected n_estimators = {best_n} (OOB score = {best_score:.4f})", module=Module.RF)
        return best_n

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
        best_n = self._auto_select_n_estimators(x_scaled, labels)
        self._clf_substance = SkRandomForest(
            n_estimators=best_n,
            random_state=42,
            n_jobs=-1
        )
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
