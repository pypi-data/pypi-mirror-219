import numpy as np
import pandas as pd


def csi_stat(dataframe_in, features_no_deseadas=["mach_id", "year", "month", "period"]):
    """
    Función para realizar análisis csi de las variables. La función
    retorna un reporte en formato dataframe del csi y estado de cada
    una de las variables.
    """

    # verificación de tipos
    if not isinstance(dataframe_in, pd.DataFrame):
        raise TypeError(
            "El argumento 'dataframe_in' debe ser de tipo 'pd.DataFrame', "
            f"se entregó {type(dataframe_in)}"
        )

    if not isinstance(features_no_deseadas, list):
        raise TypeError(
            "El argumento 'features_no_deseadas' debe ser de tipo 'list', "
            f"se entregó {type(dataframe_in)}"
        )

    data_in = dataframe_in.copy()
    data_in["period"] = data_in["year"].astype(int) * 100 + data_in["month"].astype(int)

    # Lista de comprehesion para filtrar features no deseadas
    column_period = [i for i in data_in.columns if i not in features_no_deseadas]

    # Preparamos variables para la salida
    nulls_variables = []
    df_append = pd.DataFrame()
    for a_variable in column_period:
        # Se generan quintiles según la variable
        df_feat = data_in[[a_variable, "period"]]
        quantiles = len(df_feat[a_variable].dropna().unique())
        if quantiles == 0:
            nulls_variables.append(a_variable)
            continue
        elif quantiles >= 10:
            quantiles = 10
        df_feat.loc[:, "cuantil"] = pd.cut(df_feat[a_variable], quantiles)

        # Agregación para contar casos por quintiles
        df_feat = (
            df_feat.groupby(by=["period", "cuantil"])
            .agg({a_variable: "count"})
            .reset_index()
        )
        df_feat = df_feat.pivot(index="cuantil", columns="period", values=a_variable)
        df_feat = df_feat.div(df_feat.sum(axis=0), axis=1)

        # Generamos dataframe final
        df_out = df_feat.copy()
        for i in range(df_feat.shape[1] - 1):
            actual = df_feat.iloc[:, i + 1] + 10e-20
            expected = df_feat.iloc[:, i] + 10e-20
            df_out.iloc[:, i + 1] = (actual - expected) * np.log(actual / expected)

        # Preparamos salida y append
        df_out = df_out.drop(columns=df_feat.columns[0])
        df_out = pd.DataFrame(df_out.sum()).rename(columns={0: a_variable}).T
        df_out["cuantil"] = quantiles
        df_append = pd.concat([df_append, df_out], axis=0)

    # Semaforo de estabilidad
    df_append["status"] = "🟢"
    df_append["status_2"] = "low"

    cond1 = (df_append.iloc[:, :-3] >= 0.1) & (df_append.iloc[:, :-3] < 0.2)
    cond1 = cond1.any(axis=1)

    cond2 = df_append.iloc[:, :-3] > 0.2
    cond2 = cond2.any(axis=1)

    df_append.loc[cond1, "status"] = "🟡"
    df_append.loc[cond1, "status_2"] = "medium"
    df_append.loc[cond2, "status"] = "🔴"
    df_append.loc[cond2, "status_2"] = "high"

    return df_append


def stablity_stat(
    dataframe_in, features_no_deseadas=["mach_id", "year", "month", "period"]
):
    # verificación de tipos
    if not isinstance(dataframe_in, pd.DataFrame):
        raise TypeError(
            "El argumento 'dataframe_in' debe ser de tipo 'pd.DataFrame', "
            f"se entregó {type(dataframe_in)}"
        )

    if not isinstance(features_no_deseadas, list):
        raise TypeError(
            "El argumento 'features_no_deseadas' debe ser de tipo 'list', "
            f"se entregó {type(dataframe_in)}"
        )

    data_in = dataframe_in.copy()

    # Obtenemos periodo
    data_in["period"] = data_in["year"].astype(int) * 100 + data_in["month"].astype(int)

    # Lista de comprehesion para filtrar features no deseadas
    column_period = [i for i in data_in.columns if i not in features_no_deseadas]

    # Preparamos variables para la salida
    df_append_mean, df_append_std, df_append_nulls = (
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
    )
    for a_variable in column_period:
        # Se generan quintiles según la variable
        df_feat = data_in[[a_variable, "period"]]

        # Agregación para promediar las variables
        df_feat_mean = (
            df_feat.groupby(by=["period"]).agg({a_variable: "mean"}).reset_index()
        )
        df_feat_std = (
            df_feat.groupby(by=["period"]).agg({a_variable: "std"}).reset_index()
        )
        df_feat_nulls = df_feat.copy()
        df_feat_nulls["bool"] = df_feat_nulls.isna()[a_variable]

        # procesamos mean y calculamos la diferencia porcentual entre periodos
        df_feat_mean["shift"] = df_feat_mean[a_variable].shift()
        df_feat_mean["diff_%"] = (
            np.abs(df_feat_mean[a_variable] - df_feat_mean["shift"])
            / df_feat_mean["shift"]
        )

        # Preparamos salida y append para la mean
        df_feat_mean = (
            df_feat_mean.dropna()[["period", "diff_%"]]
            .rename(columns={"diff_%": a_variable})
            .set_index("period")
            .T
        )
        df_append_mean = pd.concat([df_append_mean, df_feat_mean], axis=0)

        # Preparamos salida y append para la std
        df_feat_std = df_feat_std.set_index("period").T
        df_append_std = pd.concat([df_append_std, df_feat_std], axis=0)

        # generamos info de nulls
        a = df_feat_nulls.groupby("period").agg({"bool": "count"})
        b = df_feat_nulls.groupby("period").agg({"bool": "sum"})
        df_feat_nulls = (b * 100 / a).rename(columns={"bool": a_variable})

        # Preparamos salida de nulos
        df_feat_nulls = df_feat_nulls.T
        df_append_nulls = pd.concat(
            [df_append_nulls, df_feat_nulls], axis=0
        )

    return df_append_mean, df_append_std, df_append_nulls
