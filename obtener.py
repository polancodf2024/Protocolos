import streamlit as st
import os
from pathlib import Path
import pandas as pd

# Configuración
ARCHIVO_OBJETIVO = "registro_analisis.csv"

# Obtener el directorio actual
current_path = Path(os.getcwd())

# Buscar el archivo en el directorio actual
st.title("Lectura de registro_analisis.csv")
st.header("Búsqueda del archivo")

archivo_path = None
if (current_path / ARCHIVO_OBJETIVO).exists():
    archivo_path = current_path / ARCHIVO_OBJETIVO
    st.success(f"Archivo encontrado en: {archivo_path}")
else:
    # Buscar en subdirectorios
    for subdir in current_path.iterdir():
        if subdir.is_dir() and (subdir / ARCHIVO_OBJETIVO).exists():
            archivo_path = subdir / ARCHIVO_OBJETIVO
            st.success(f"Archivo encontrado en: {archivo_path}")
            break

# Mostrar contenido del archivo si se encuentra
if archivo_path:
    try:
        st.header("Contenido del archivo")
        df = pd.read_csv(archivo_path)
        st.dataframe(df)
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
else:
    st.error(f"No se encontró el archivo {ARCHIVO_OBJETIVO} en el directorio actual ni en los subdirectorios.")

# Descargar el archivo encontrado (opcional)
if archivo_path:
    st.header("Descargar archivo")
    with open(archivo_path, "rb") as file:
        st.download_button(
            label=f"Descargar {ARCHIVO_OBJETIVO}",
            data=file,
            file_name=ARCHIVO_OBJETIVO,
            mime="text/csv"
        )

