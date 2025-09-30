#!/usr/bin/env python3
import random
from copy import deepcopy
from typing import List, Dict, Any, Tuple

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

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
        # return [(d['label'] + ' ' + d.get('quantity', '')).strip().lower() for d in data], [d['data'] for d in data]
        # TODO quantities disabled for thesis test
        return [(d['label']).strip().lower() for d in data], [d['data'] for d in data]

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

    @staticmethod
    def _group_sequences(labels: List[str], data: List[List[float]]) -> List[Dict[str, Any]]:
        """
        Groups contiguous samples by label changes.
        """
        groups = []
        current_label, current_data = labels[0], []

        for lbl, sample in zip(labels, data):
            if lbl != current_label:
                groups.append({"label": current_label, "data": current_data})
                current_label, current_data = lbl, []
            current_data.append(sample)
        groups.append({"label": current_label, "data": current_data})
        return groups

    @staticmethod
    def _split_groups(groups: List[Dict[str, Any]], train_ratio: float = 0.7, seed: int = 42):
        """
        Splits groups into train/test while preserving contiguity and balancing labels.
        """
        random.seed(seed)
        by_label = {}

        # Organize groups by label
        for g in groups:
            by_label.setdefault(g["label"], []).append(g)

        train_data, test_data = [], []

        for lbl, g_list in by_label.items():
            random.shuffle(g_list)

            if len(g_list) == 1:
                # only one group → force it into train
                train_data.extend(g_list)
            else:
                split_idx = max(1, int(len(g_list) * train_ratio))
                split_idx = min(len(g_list) - 1, split_idx)  # leave at least one for test
                train_data.extend(g_list[:split_idx])
                test_data.extend(g_list[split_idx:])

        return train_data, test_data

    @staticmethod
    def _prepare_balanced_data(
            groups: List[Dict[str, Any]],
            balance: bool = True,
            strategy: str = "oversample"  # "undersample" | "oversample"
    ):
        """
        Converts grouped data into flat X, y lists.

        Balancing strategies:
          - "undersample": reduce larger groups down to the smallest size.
          - "oversample": increase smaller groups up to the largest size.
        """
        x, y = [], []
        for g in groups:
            x.extend(g["data"])
            y.extend([g["label"]] * len(g["data"]))

        if not balance or len(set(y)) <= 1:
            return x, y

        counts = {lbl: y.count(lbl) for lbl in set(y)}

        if strategy == "undersample":
            target_count = min(counts.values())
        elif strategy == "oversample":
            target_count = max(counts.values())
        else:
            raise ValueError(f"Unknown balancing strategy: {strategy}")

        x_bal, y_bal = [], []
        for lbl in set(y):
            lbl_samples = [(xx, yy) for xx, yy in zip(x, y) if yy == lbl]

            if strategy == "undersample":
                sampled = random.sample(lbl_samples, target_count)
            else:  # oversample
                sampled = random.choices(lbl_samples, k=target_count)

            for sample_x, sample_y in sampled:
                x_bal.append(sample_x)
                y_bal.append(sample_y)

        return x_bal, y_bal

    @staticmethod
    def save_confusion_matrix(y_true, y_pred, labels, title, filename):
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)

        # Title and colorbar
        ax.set_title(title)
        plt.colorbar(im, ax=ax)

        # Tick marks and labels
        tick_marks = np.arange(len(labels))
        ax.set_xticks(tick_marks)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_yticks(tick_marks)
        ax.set_yticklabels(labels)

        # Annotate cells
        thresh = cm.max() / 2.0
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(
                    j, i, format(cm[i, j], "d"),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black"
                )

        ax.set_ylabel("True label")
        ax.set_xlabel("Predicted label")
        fig.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
        log.info(f"Confusion matrix saved to {filename}", module=Module.RF)

    def _train_models(self) -> Dict[str, MLAdapter]:
        """
        Trains all available ML models and returns them as a dict of names to MLAdapter objects.
        :return: the dictionary of names to MLAdapter objects.
        """
        _labels, _data = self._get_available_data()
        groups = self._group_sequences(_labels, _data)
        train_groups, test_groups = self._split_groups(groups, train_ratio=0.7)
        x_train, y_train = self._prepare_balanced_data(train_groups, balance=True)
        x_test, y_test = self._prepare_balanced_data(test_groups, balance=True)

        unique_train, counts_train = np.unique(y_train, return_counts=True)
        unique_test, counts_test = np.unique(y_test, return_counts=True)

        print("Train label distribution:")
        for label, count in zip(unique_train, counts_train):
            print(f"  {label}: {count}")

        print("\nTest label distribution:")
        for label, count in zip(unique_test, counts_test):
            print(f"  {label}: {count}")

        classifiers: Dict[str, MLAdapter] = {}
        for i, model_name in enumerate(ml_handler.get_available_models()):
            try:
                log.info(f'Training {model_name} classifier...', module=Module.PRE)
                _classifier = self._train_model(x_train, y_train, i)
                y_pred = _classifier.predict(x_test)
                report = classification_report(y_test, y_pred, digits=3)
                self.save_confusion_matrix(
                    y_test,
                    y_pred,
                    _classifier.classes_,
                    "Substance Classifier Confusion Matrix",
                    f"{model_name}_confusion_matrix_substances.png"
                )
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
