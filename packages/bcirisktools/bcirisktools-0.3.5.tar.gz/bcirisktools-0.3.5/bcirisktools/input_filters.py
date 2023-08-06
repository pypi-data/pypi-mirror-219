import sys
from typing import Tuple

import numpy as np
import pandas as pd

from bcirisktools.metrics_bci import MetricsBCI


class InputTreatment:
    def __init__(self, data, variables, model_label):
        self.variables = variables
        self.model_label = model_label
        self.univariate_table, self.selected_vars = self.univ_predict(
            data, self.variables, self.model_label
        )

    def filt_corr(self, df_in, corr_threshold=0.7, method="pearson", family=False):
        pred_var = self.univariate_table
        if family:
            pred_var["Group"] = "SinGrupo"

        selected_variables = []
        for group in pred_var["Group"].unique():
            variables = pred_var[pred_var["Group"] == group]["Feature"]
            selected_variables.append(self._identify_correlated(df_in[variables], 0.9))
        seleccionadas = self._flatten(selected_variables)

        print(f"\nVariables candidatas iniciales: {len(self.selected_vars)}")
        print(f"\nSeleccionadas por correlación familiar: {len(seleccionadas)}")
        return seleccionadas

    @staticmethod
    def univ_predict(df_in, variables, model_label):
        data_model = df_in.copy()
        pred_var = []
        total_variables = len(variables)

        for it, f in enumerate(variables):
            sys.stdout.write(f"\rProcesando [{it+1}/{total_variables}]" + "\r")
            metricas = MetricsBCI.evaluate(
                data_model[model_label], data_model[f].astype(float)
            )
            grupo_var = f.split("_")[0]
            pred_var.append([f, grupo_var, metricas[0], metricas[1], metricas[2]])

        pred_var = pd.DataFrame(
            pred_var, columns=["Feature", "Group", "ROC", "KS", "DIV"]
        )

        # En base a criterios de KS y ROC se selecciona las Variables que sobrepasen
        # un valor al ser consideradas predictivas.
        print(
            f"Variables candidatas iniciales: {len(variables)}",
        )
        pred_var_filtered = pred_var.loc[
            (pred_var["KS"] > 0.01) & (pred_var["ROC"] > 0.501), :
        ]
        seleccionadas = list(pred_var_filtered["Feature"].values)
        print(f"\nSeleccionadas por univariado: {len(seleccionadas)}")

        return pred_var_filtered, seleccionadas

    @staticmethod
    def filldata(df_in, num_value=-999999, cat_value="unk"):
        data = df_in.copy()
        for col in data.columns:
            try:
                data[col] = data[col].fillna(num_value)
            except:
                data[col] = data[col].cat.add_categories(cat_value)
                data[col] = data[col].fillna(cat_value, inplace=True)

        return data
    
    @staticmethod
    def select_k_percentile(df_input, label_name, vars_no_considerar=None, fill_nan = -9999):
    
        # Select targets and features from the input data
        labels = df_input.loc[:, label_name]
        if (np.array(vars_no_considerar) != None).any():
            features = df_input.drop(columns=vars_no_considerar)
        else:
            features = df_input.drop(label_name)

        # Holdout
        X_train, X_test, y_train, y_test = train_test_split(
            features,
            labels,
            test_size=0.2,
            random_state=42,
            shuffle=True,
            stratify=labels,
        )

        def train_and_evaluate(
            pipe, print_=True, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
        ):
            """function to train and evaluate the selection pipeline using the f1-score"""

            pipe.fit(X_train, y_train)
            y_pred = pipe.predict(X_test)
            return f1_score(y_test, y_pred, average="macro")

        # Pipeline creation
        selection_pipeline = Pipeline(
            steps=[
                ("Preprocessing", SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=fill_nan)),
                ("Selection", SelectPercentile(mutual_info_classif, percentile=20)),
                ("Tree", DecisionTreeClassifier(random_state=42)),
            ]
        )

        # Loop to search the best k porcentage for the dataset
        f1 = []
        features_dict = {}
        for i in range(10, 101, 10):
            print(f"Percentil: {i}%", end="\r")
            selection_pipeline.steps[1][1].percentile = i
            f1.append([i, train_and_evaluate(selection_pipeline, print_=False)])
            features_selected = selection_pipeline.feature_names_in_[selection_pipeline[1].get_support()]
            features_dict[i] = features_selected
        f1 = np.array(f1)

        # Final Plot
        fig = px.line(
            x=f1[:, 0],
            y=f1[:, 1],
            title="F1 según cantidad de Features Conservadas",
        )

        # Update figure
        fig.update_layout(xaxis_title="Cantidad de variables", yaxis_title="F1 Score")

        # Return features list
        return features_dict

    @staticmethod
    def _flatten(list_):
        return [item for sublist in list_ for item in sublist]

    @staticmethod
    def _identify_correlated(df, threshold):
        """
        A function to identify highly correlated features.
        """
        # Compute correlation matrix with absolute values
        matrix = df.corr(method="spearman").abs()

        # Create a boolean mask
        mask = np.triu(np.ones_like(matrix, dtype=bool))

        # Subset the matrix
        reduced_matrix = matrix.mask(mask)

        # Find cols that meet the threshold
        to_drop = [
            c for c in reduced_matrix.columns if not any(reduced_matrix[c] > threshold)
        ]

        return to_drop
