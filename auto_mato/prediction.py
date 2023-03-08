# -*- coding: utf-8 -*-
"""
prediction.py

@author: Team AutoMato
"""
import pickle
from typing import List

import numpy as np


class Predictor:
    def __init__(self, model_file: str) -> None:
        """Helper class to load and use ready scikit-learn model.

        Parameters
        ----------
        model_file: Pickled scikit-learn model file.
        """
        with open(model_file, "rb") as file:
            self.model = pickle.load(file)

    def predict(self, data: np.ndarray) -> List[float]:
        """ Returns predicted value.

        Parameters
        ----------
        data: Input data for the predictor model.

        Returns
        -------
        prediction: np.ndarray
        """
        return self.model.predict(data).item()

    def switch_model(self, new_model: str) -> None:
        """Switches current model with the new one.

        Parameters
        ----------
        new_model: Pickled scikit-learn model file.
        """
        with open(new_model, "rb") as file:
            self.model = pickle.load(file)
