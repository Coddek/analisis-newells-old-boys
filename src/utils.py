import pandas as pd

def cargar_datos(path):
    """Carga el archivo Excel y devuelve un DataFrame."""
    return pd.read_excel(path)

def agrupar_datos(df, columna, operacion):
    """Agrupa datos según la columna y operación especificada."""
    return df.groupby(columna).agg(operacion).reset_index()