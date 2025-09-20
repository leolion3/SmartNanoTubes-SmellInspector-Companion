#!/usr/bin/env python3
from typing import List

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

from logging_framework.log_handler import Module, log
from ml_adapters.abstract_ml_adapter import MLAdapter


class XGBoostClassifier(MLAdapter):
    """
    Implements a multi-class classifier using XGBoost.
    Unlike the RandomForestClassifier adapter, this does not
    split into binary steps, but directly predicts among all available classes.
    Handles class imbalance using sample weights.
    """

    def __init__(self, n_estimators: int = 300, learning_rate: float = 0.1, max_depth: int = 6):
        """
        Default constructor.
        :param n_estimators: number of boosting rounds.
        :param learning_rate: step size shrinkage used in update.
        :param max_depth: maximum depth of trees.
        """
        self._scaler: StandardScaler = StandardScaler()
        self._clf = XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42,
            use_label_encoder=False,
            eval_metric="mlogloss",
        )

    def fit(self, data: List[List[float]], labels: List[str]) -> None:
        """
        Train the XGBoost classifier with class imbalance handling.
        :param data: the training data.
        :param labels: the training labels.
        :return:
        """
        log.info("Training XGBoost Classifier...", module=Module.XGB)

        # Scale data
        log.info("Scaling data...", module=Module.XGB)
        x_scaled = self._scaler.fit_transform(data)

        # Train/validation split
        x_train, x_val, y_train, y_val = train_test_split(
            x_scaled, labels, test_size=0.2, stratify=labels, random_state=42
        )

        # Compute class-balanced weights
        log.info("Computing sample weights for class imbalance...", module=Module.XGB)
        sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)

        # Fit model with weights
        log.info("Fitting multi-class XGBoost model with class balancing...", module=Module.XGB)
        self._clf.fit(x_train, y_train, sample_weight=sample_weights)

        # Evaluate validation accuracy and per-class metrics
        acc_val = self._clf.score(x_val, y_val)
        log.info(f"Validation accuracy: {acc_val:.3f}", module=Module.XGB)

        y_pred = self._clf.predict(x_val)
        report = classification_report(y_val, y_pred, zero_division=0)
        log.info("Per-class performance:\n" + report, module=Module.XGB)

    def predict(self, data: List[List[float]]) -> List[str]:
        """
        Predict labels for given samples.
        :param data: input data.
        :return: predicted labels.
        """
        x_scaled = self._scaler.transform(data)
        preds = self._clf.predict(x_scaled)
        return preds.tolist()
