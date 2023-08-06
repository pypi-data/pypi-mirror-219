from typing import Tuple, Union

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score


class MetricsBCI:
    @staticmethod
    def evaluate(
        y_true: Union[pd.Series, np.ndarray],
        y_pred: Union[pd.Series, np.ndarray],
        verbose=0,
    ) -> Tuple[np.number, np.number, np.number]:
        """Evalua calculando 3 indicadores de desempeño: ROC AUC, KS y Divergencia.

        Parameters
        ----------
        y_true : Union[pd.Series, np.ndarray]
            Arreglo o Serie con la variable objetivo.
        y_pred : Union[pd.Series, np.ndarray]
            Arreglo o Serie con los datos predichos por el modelo ya entrenado.
        verbose : int, optional
            1 imprime los estadísticos, 0 omite la impresión, by default 0.

        Returns
        -------
        Tuple[np.number, np.number, np.number]
            Tupla que contiene el estadístco AUC ROC, KS y Div.
        """
        x = y_pred[y_true == 1]
        y = y_pred[y_true == 0]

        a1 = roc_auc_score(y_true, y_pred)
        a1 = max(a1, 1 - a1)

        a2 = ks_2samp(x, y)

        var_m = np.var(x) + np.var(y)
        if var_m > 0:
            a3 = (2 * (x.mean() - y.mean()) ** 2) / var_m
        else:
            a3 = -1
        if verbose > 0:
            print(
                "ROC {:0.2f} | KS {:0.2f} | DIV {:0.2f} ".format(a1, a2.statistic, a3)
            )

        return a1, a2.statistic, a3
