import base64
import os
import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import shap
import xgboost as xgb
from scipy.stats import ks_2samp
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


class GenerateReport:
    def __init__(
        self,
        x,
        y,
        params,
        min_value=-9999,
        report_name="report",
        model=None,
        name="model",
        order_by="Mean Shapley",
        rng=0,
    ):
        self.name_report = name
        self.order_by = order_by
        self.min_value = min_value
        # initializate creating values for the analysis
        if model is None:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                x, y, test_size=0.2, random_state=rng
            )
        else:
            self.X_train = x
            self.y_train = y
        # Define model's variables and model XGBoost
        self.model = model
        self.param = params
        self.report_name = report_name

    def _evaluate(self, y_true, y_pred, verbose=0, mode="tuple"):
        a1 = roc_auc_score(y_true, y_pred)
        a1 = max(a1, 1 - a1)

        a2 = ks_2samp(y_pred[y_true == 1], y_pred[y_true == 0])

        x = y_pred[y_true == 1]
        y = y_pred[y_true == 0]

        var_m = np.var(x) + np.var(y)
        if var_m > 0:
            a3 = (2 * (x.mean() - y.mean()) ** 2) / var_m
        else:
            a3 = -1
        if verbose > 0:
            print(
                "ROC {:0.2f} | KS {:0.2f} | DIV {:0.2f} ".format(a1, a2.statistic, a3)
            )
        r = (a1, a2.statistic, a3)
        if mode == "tuple":
            return r
        if mode == "full":
            return a1, a2.statistic, a3

    def _univariate_analysis(self):
        self.predVar = []
        variables = self.X_train.columns
        total_variables = len(variables)

        for it, f in enumerate(variables):
            sys.stdout.write(f"\rVariable analyzed: {f} [{it+1}/{total_variables}]")
            sys.stdout.write("\033[K")
            results = self._evaluate(self.y_train, self.X_train[f].values)
            grupo_var = f.split("_")[0]

            self.predVar.append([f, grupo_var, results[0], results[1], results[2]])
        self.predVar = pd.DataFrame(
            self.predVar, columns=["Features", "Group", "ROC", "KS", "DIV"]
        )
        self.predVar = self.predVar.loc[
            (self.predVar["KS"] > 0.01) & (self.predVar["ROC"] > 0.501), :
        ]
        self.variables_univariate = self.predVar["Features"]

    def _plot_shaps(self, study_var, x_label="", shap_nulls=False):
        if shap_nulls:
            cond = self.X_train[study_var].values >= self.min_value
            shaps_values = self.shap_values.values[... , -1][cond]
            inputs_x = self.X_train[cond]
        else:
            
            shaps_values = self.shap_values.values[... , -1]
            inputs_x = self.X_train

        shap.dependence_plot(
            study_var,
            shaps_values,
            inputs_x,
            xmin="percentile(0.5)",
            xmax="percentile(99)",
            dot_size=4,
            interaction_index=None,
            show=False,
        )

        # plt.title("Variable: "+ str(study_var))
        # plt.ylabel("SHAP value")
        # plt.xlabel(str(x_label))
        plt.axhline(y=0, color="darkred", linestyle="-")
        if shap_nulls:
            plt.savefig(f"./plot/{study_var}_nulls.png")
        else:
            plt.savefig(f"./plot/{study_var}.png")
        plt.close()

    def analyze_data(self):
        # Univariate analysis
        print("/------------------------------------------------------/")
        print("Initializing univariate analysis...")
        print("/------------------------------------------------------/")
        self._univariate_analysis()

        # Redefine data
        self.X_train = self.X_train

        # Get Shapley values
        print("\n/------------------------------------------------------/")
        print("Calculating Shapley values...")
        print("/------------------------------------------------------/")
        if self.model is None:
            self.dtrain = xgb.DMatrix(self.X_train, label=self.y_train)
            self.model = xgb.train(self.param, self.dtrain, 530)
        explainer = shap.TreeExplainer(self.model)
        self.shap_values = explainer(self.X_train)

        var_names = self.shap_values.feature_names
        var_shap = np.abs(self.shap_values.values).mean(axis=0)

        self.df_shap = pd.DataFrame(
            zip(var_names, var_shap[:, -1]), columns=["Features", "Mean Shapley"]
        )
        self.df_shap = self.df_shap.sort_values(
            by="Mean Shapley", ascending=False
        ).reset_index(drop=True)
        self.df_shap_top = self.df_shap.head(10)

        # Final Dataframe
        self.df_shap = self.df_shap.merge(self.predVar)[
            ["Features", "Group", "ROC", "KS", "DIV", "Mean Shapley"]
        ].sort_values(by=self.order_by, ascending=False)

        # Summary plot
        fig_shap_bar = px.bar(
            self.df_shap_top.sort_values(by="Mean Shapley", ascending=True),
            x="Mean Shapley",
            y="Features",
            title="Resumen de Valores de Shapley",
            orientation="h",
        )

        # Create directory
        mypath = "./plot/"
        if not os.path.isdir(mypath):
            os.mkdir(mypath)
        else:
            shutil.rmtree(mypath)
            os.mkdir(mypath)

        # Get plots
        print("Generating Shapley plots...")
        print("/------------------------------------------------------/")
        for idx, var in enumerate(self.df_shap["Features"]):
            sys.stdout.write(f"\rVariable analyzed: {var} [{idx+1}]")
            try:
                self._plot_shaps(var, "", shap_nulls=False)
                self._plot_shaps(var, "", shap_nulls=True)
            except:
                sys.stdout.write(f"\rVariable not analyzed: {var} [{idx+1}]")

        # Generate report
        print("\n/------------------------------------------------------/")
        print("Generating Html Report...")
        print("/------------------------------------------------------/")

        imgs_in_folder = [
            img_in_folder
            for img_in_folder in os.listdir(mypath)
            if "_nulls.png" not in img_in_folder
        ]

        df_html = self.df_shap.to_html()
        for idx, img_to_html in enumerate(imgs_in_folder):
            df_html = df_html.replace(
                f'<td>{img_to_html.split(".")[0]}</td>\n',
                f'<td><a href="#{img_to_html.split(".")[0]}">'
                f'{img_to_html.split(".")[0]}</a></td>\n',
            )
        df_html = df_html.replace(
            '<table border="1" class="dataframe">',
            '<table class="table table-striped">',
        )

        html_string = (
            """
        <html>
            <head>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                <style>body{ margin:0 100; background:whitesmoke; }</style>
            </head>
            <body>
                <h1>Resumen del Modelo: """
            + self.name_report
            + """</h1>
                """
            + fig_shap_bar.to_html()
            + """
                <hr class="solid">
                <h2>Sección 2: DataFrame de Resumen</h2>
                <a id="summary"></a>
                <center>
                """
            + df_html
            + """
                </center>
                <hr class="solid">
                <h2>Sección 3: Dependencies Plot</h2>
        """
        )  # ignore: E501

        for idx, img_to_html in enumerate(imgs_in_folder):
            if "nulls.png" not in img_to_html:
                data_uri_1 = base64.b64encode(
                    open("./plot/" + img_to_html, "rb").read()
                ).decode("utf-8")
                try:
                    data_uri_2 = base64.b64encode(
                        open(
                            "./plot/" + img_to_html.replace(".png", "_nulls.png"), "rb"
                        ).read()
                    ).decode("utf-8")
                except:
                    print(img_to_html.replace(".png", "_nulls.png"), "No existe")
                    data_uri_2 = None
            html_string = (
                html_string
                + """
              <h3><b>ID: """
                + str(idx + 1)
                + '''</b></h3>
              <a id="'''
                + img_to_html.split(".")[0]
                + """"></a>
              <h3><b>Variable: """
                + img_to_html.split(".")[0]
                + """</b></h3>
              <br>
              <p> Variables con Nulos </p>
              """
                + '<img src="data:image/png;base64,{0}" class="center">'.format(
                    data_uri_1
                )
            )

            if data_uri_2 is not None:
                html_string = (
                    html_string
                    + """
                <br>
                  <p> Variables sin Nulos </p>
                  """
                    + '<img src="data:image/png;base64,{0}" class="center">'.format(
                        data_uri_2
                    )
                )

            html_string = (
                html_string
                + """
              <br>
              <a href="#summary">VOLVER AL INICIO</a>
              <hr class="solid">
            """
            )

        print("Process completed :)")
        print("/------------------------------------------------------/")

        html_string = html_string + "</body></html>"
        f = open(f"./{self.report_name}.html", "w")
        f.write(html_string)
        f.close()

        # Removemos la carpeta temporal de plots
        shutil.rmtree(mypath)