#!/usr/bin/env python3
from typing import override, List

from sklearn.model_selection import train_test_split
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
        self._clf_air = SkRandomForest(n_estimators=n_estimators, random_state=42)
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

        # Scale data
        log.info('Scaling data...', module=Module.RF)
        x_scaled = self._scaler.fit_transform(data)

        # Step 1: Air vs Not-Air
        y_binary = ["air" if lbl == "air" else "not-air" for lbl in labels]
        x_train, x_val, y_train, y_val = train_test_split(
            x_scaled, y_binary, test_size=0.2, stratify=y_binary, random_state=42
        )
        log.info('Fitting air detector...', module=Module.RF)
        self._clf_air.fit(x_train, y_train)
        acc_air = self._clf_air.score(x_val, y_val)
        log.info(f'Air detection accuracy: {acc_air:.3f}', module=Module.RF)

        # Step 2: Domol vs Octeniderm (non-air only)
        mask = [lbl != "air" for lbl in labels]
        x_substances = [x for x, m in zip(x_scaled, mask) if m]
        y_substances = [lbl for lbl in labels if lbl != "air"]

        if len(set(y_substances)) > 1:
            xs_train, xs_val, ys_train, ys_val = train_test_split(
                x_substances, y_substances, test_size=0.2, stratify=y_substances, random_state=42
            )
            log.info('Fitting substance classifier...', module=Module.RF)
            self._clf_substance.fit(xs_train, ys_train)
            acc_sub = self._clf_substance.score(xs_val, ys_val)
            log.info(f'Substance classification accuracy: {acc_sub:.3f}', module=Module.RF)
        else:
            log.warning('Only one substance class present, skipping step 2 training.', module=Module.RF)

    @override
    def predict(self, data: List[List[float]]) -> List[str]:
        """
        Predict labels for given samples.
        :param data: input data.
        :return: predicted labels.
        """
        x_scaled = self._scaler.transform(data)
        preds = []
        for sample in x_scaled:
            sample_reshaped = sample.reshape(1, -1)
            if self._clf_air.predict(sample_reshaped)[0] == "air":
                preds.append("air")
            else:
                preds.append(str(self._clf_substance.predict(sample_reshaped)[0]))
        return preds
