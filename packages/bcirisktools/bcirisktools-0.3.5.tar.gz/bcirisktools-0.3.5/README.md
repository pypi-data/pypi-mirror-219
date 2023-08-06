![BCI LOGO](https://cdn3.bci.cl/uploads/f67e8ed8-04ed-4dc9-a433-683404c8ea06/original/logo_Bci_Vcb.png)

# BCIRISKTOOLS V.0.2: Herramientas de Modelamiento de Riesgo

BciRiskTools es una librería enfocada en la democratización del conocimiento y herramientas para el modelamiento y procesamiento de datos. Dentro de los recursos que ofrece la librería se encuentra análisis de estabilidad de las variables, selección de variables, métricas de evaluación y generación de intervalos en base a árboles de decisión.

## Instalación

bcirisktool puede ser instalado utilizando [Pypi](https://pypi.org/project/bcirisktools/), para esto utilizar el siguiente comando en su jupyter notebook o consola:

**Jupyter:**
En una celda escribir

```python
!pip install bcirisktools
```

**Shell:**
En una consola con **pip** instalado usar

```shell
pip install bcirisktools
```

## ¿Cómo usar esta librería?

### Estabilidad de Variables

Para medir la estabilidad de variables se tiene la función `csi_stat` quien calcula el estadístico llamado `characteristic stability index` (csi). Para ejecutar la función se debe entregar un dataframe formato `pandas.DataFrame` con las variables que se desean analizar. Dentro de la estructura a considerar para el dataframe es que esté debe contener el `year`, `month` y `period`. Por otro lado, en el argumento de entrada `vars_no_considerar` se debe señalar las variables que no son necesarias en el análisis de estabilidad, por ello se debe especificar que no se analizará un: rut, año, mes u variables que no forman parte de comportamientos. El resultado de la función entrega el estadístico CSI para cada una de las variables en un dataframe formato `pandas.DataFrame`, en el dataframe cada fila representará a una variable y su estabilidad señalada por un semáforo: rojo es alta inestabilidad, amarillo riesgo medio y verde sin riesgo.

```python
import bcirisktools

df_csi = bcirisktools.csi_stat(df, vars_no_considerar=['mach_id', 'year', 'month', 'period'])
```

![EJEMPLO TABLA](./images/tabla_example.PNG)

Una segunda función es `stablity_stat()` quien bajo el mismo formato de entrada que la función anterior obtiene estadísticos extra para el análisis de la estabilidad. Dentro de las salidas encontraremos un estadístico de las medias, desviaciones estándares  y nulos en el tiempo en el tiempo.

```python
import bcirisktools

df_append_mean, df_append_std, df_append_nulls = bcirisktools.stablity_stat(df, vars_no_considerar)
```



### Generación de Intervalos

Una de las herramientas mas relevantes es la creación de intervalos en base a árboles de decisión. Dentro de los puntos relevantes en esta herramienta se encuentra tanto la creación de intervalos y la medición de riesgo que posee cada uno de estos intervalos, visualizando con ello el riesgo y la predictibilidad que poseen diferentes variables respecto a una variable de desempeño. El resultado final de estas funciones es un reporte en formato **.html** que permite un análisis mas profundo de cada una de las variables.

Para ejecutar la herramienta se debe generar un dataframe que posea las **variables a analizar** y la **variable de desempeño** que se desea utilizar. Para elaborar el ejemplo se ha considerado como dataframe de entrada a **df_banked**, la variable de desempeño **flag_30d_3m_ever** y eñ report_name se refiere al nombre del archivo **.html** a crear.

```python
import bcirisktools

intervalos_variables_grupal, intervalos_predicciones_variable_grupal = bcirisktools.run_crt_tree(df_banked, "flag_30d_3m_ever", max_depth=2)
estadisticos_resumen_grupal = bcirisktools.get_statistics(intervalos_predicciones_variable_grupal)
bcirisktools.get_report(estadisticos_resumen_grupal, report_name="reporte_banked")
```

Finalmente, el reporte es generado en la misma ubicación del archivo donde se ejecutan los comandos, generando:

![EJEMPLO REPORTE](./images/reporte_example.PNG)

## ¿ Como puedo actualizar la librería en Pypi?

Para actualizar la versión de la librería usted deberá actualizar la versión de la librería en el archivo `setup.py` y luego ejecutar el siguiente script en la raíz del archivo utilizando el terminal:

```shell
python setup.py sdist
twine upload dist/*
```