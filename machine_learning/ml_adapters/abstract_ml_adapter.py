#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List, Optional


class MLAdapter(ABC):
    """
    Abstract interface for ML adapters.
    """

    @abstractmethod
    def fit(self, data: List[List[float]], labels: List[str]) -> None:
        """
        Train the ML model with the given labeled data.
        :param data: the training/test data.
        :param labels: the training labels.
        :return:
        """
        pass

    @abstractmethod
    def predict(self, data: List[List[float]]) -> List[str]:
        """
        Make predictions for the given dataset.
        :param data: the dataset to make predictions for.
        :return: the prediction labels.
        """
        pass

    @property
    def classes_(self) -> List[str]:
        """
        Optional: return the class labels learned by the model.
        Default: empty list (subclasses should override if applicable).
        """
        return []
