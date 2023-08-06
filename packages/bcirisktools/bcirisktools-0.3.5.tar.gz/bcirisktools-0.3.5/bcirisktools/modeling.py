import sys

# Estructuras de datos
import numpy as np
import pandas as pd

# interpretability
import shap

# XGBoost model
import xgboost as xgb
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import recall_score

# Scikit learn library
from sklearn.model_selection import (
    GridSearchCV,
    RepeatedStratifiedKFold,
    train_test_split,
)
from xgboost import XGBClassifier


class ModelTools:
    @staticmethod
    def analyze_imbalance(X, y, model, weights, metric_score="roc_auc"):
        param_grid = {"scale_pos_weight": weights}
        # Procedimiento de evaluación
        print("Inicializando GridSearch para ajustar balance de datos..")
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        grid = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            n_jobs=-1,
            cv=cv,
            scoring=metric_score,
        )
        # Entrenar la grid search
        grid_result = grid.fit(X, y)
        # Salida
        print(
            f"Mejor score: {grid_result.best_score_} usando {grid_result.best_params_}"
        )
        # valores obtenidos en las metricas
        means = grid_result.cv_results_["mean_test_score"]
        stds = grid_result.cv_results_["std_test_score"]
        params = grid_result.cv_results_["params"]
        for mean, stdev, param in zip(means, stds, params):
            print(f"{mean} ({stdev}) con: {param}")

    @staticmethod
    def select_variables_importance(X, y, min_features):
        # Inicializamos lista vacia para guardar valores
        list_variables = []
        # Separamos los datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=31415, stratify=y
        )
        # Ajustamos el modelo
        model = XGBClassifier()
        model.fit(X_train, y_train)
        # obtenemos las predicciones y el accuracy del modelo
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        recall = recall_score(y_test, predictions)

        list_variables.append((0, X_train.shape[1], [X_train.columns], recall * 100.0))

        thresholds = np.unique(sorted(model.feature_importances_))
        for thresh in thresholds:
            # Seleccionamos las variables utilizando treshhold
            selection = SelectFromModel(model, threshold=thresh, prefit=True)

            select_X_train = selection.transform(X_train)
            # entrenamos modelo
            selection_model = XGBClassifier(scale_pos_weight=99)
            selection_model.fit(select_X_train, y_train)
            # evaluamos modelo
            select_X_test = selection.transform(X_test)
            y_pred = selection_model.predict(select_X_test)
            predictions = [round(value) for value in y_pred]
            recall = recall_score(y_test, predictions)

            if select_X_train.shape[1] >= min_features:
                list_variables.append(
                    (
                        thresh,
                        select_X_train.shape[1],
                        [selection.get_support()],
                        recall * 100.0,
                    )
                )
                sys.stdout.write(
                    "\r Running... Thresh=%.5f, n=%d, Recall: %.2f%%"
                    % (thresh, select_X_train.shape[1], recall * 100.0)
                )
            else:
                break

        return list_variables

    @staticmethod
    def select_variables_shap(X, y, min_features):
        # Inicializamos lista vacia para guardar valores
        list_variables = []
        # Separamos los datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=31415, stratify=y
        )
        # Ajustamos el modelo
        model = XGBClassifier()
        model.fit(X_train, y_train)
        # obtenemos las predicciones y el accuracy del modelo
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        recall = recall_score(y_test, predictions)

        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_train)

        var_names = shap_values.feature_names
        var_shap = np.abs(shap_values.values).mean(axis=0)

        df_shap = pd.DataFrame(
            zip(var_names, var_shap), columns=["Features", "Mean Shapley"]
        )
        df_shap = df_shap.sort_values(by="Mean Shapley", ascending=False).reset_index(
            drop=True
        )

        list_variables.append(
            (0, X_train.shape[1], df_shap["Features"].values, recall * 100)
        )

        n_vars = float("inf")
        threshold_shap = df_shap["Mean Shapley"].min()
        while n_vars > min_features:
            # Seleccionamos las variables utilizando treshhold
            select_X = df_shap[df_shap["Mean Shapley"] > threshold_shap]["Features"]
            select_X_train = X_train[select_X]
            n_vars = select_X_train.shape[1]
            # entrenamos modelo
            model = XGBClassifier(scale_pos_weight=99)
            model.fit(select_X_train, y_train)
            # calculamos shapley values
            explainer = shap.TreeExplainer(model)
            shap_values = explainer(select_X_train)
            # Obtenemos nombre de vars y valores
            var_names = shap_values.feature_names
            var_shap = np.abs(shap_values.values).mean(axis=0)
            # Creamos dataframe
            df_shap = pd.DataFrame(
                zip(var_names, var_shap), columns=["Features", "Mean Shapley"]
            )
            df_shap = df_shap.sort_values(
                by="Mean Shapley", ascending=False
            ).reset_index(drop=True)
            # evaluamos modelo
            select_X_test = X_test[select_X]
            y_pred = model.predict(select_X_test)
            predictions = [round(value) for value in y_pred]
            recall = recall_score(y_test, predictions)

            list_variables.append(
                (threshold_shap, n_vars, df_shap["Features"].values, recall * 100.0)
            )
            sys.stdout.write(
                "\r Running... Thresh=%.5f, n=%d, Recall: %.2f%%"
                % (threshold_shap, n_vars, recall * 100.0)
            )
            threshold_shap = df_shap["Mean Shapley"].min()

        return list_variables

    @staticmethod
    def model_wrapper(X, y, params=None):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=31415, stratify=y
        )

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_test, label=y_test)

        if params is None:
            param = {
                "max_depth": 4,
                "eta": 0.03,
                "gamma": 0.6000000000000001,
                "max_delta_step": 4.0,
                "reg_alpha": 1.6,
                "reg_lambda": 0.65,
                "colsample_bytree": 0.15000000000000002,
                "min_child_weight": 300.0,
                "subsample": 0.6000000000000001,
                "objective": "binary:logistic",
                "eval_metric": "auc",
                "seed": 18283,
            }
        num_round = 1200

        model = xgb.train(param, dtrain, num_round, verbose_eval=False)

        # Predicciones en entrenamiento y test
        ypred_train = model.predict(dtrain)
        ypred_val = model.predict(dval)

        return model, ypred_train, ypred_val
