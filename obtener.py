import streamlit as st
import os
from pathlib import Path
import pandas as pd

# Configuración
ARCHIVO_OBJETIVO = "registro_analisis.csv"
DIRECTORIO_RAIZ = Path("/")  # Define la raíz para iniciar la búsqueda

# Función para buscar el archivo recursivamente
def buscar_archivo_recursivamente(directorio_raiz, archivo_objetivo):
    for root, dirs, files in os.walk(directorio_raiz):
        if archivo_objetivo in files:
            return Path(root) / archivo_objetivo
    return None

# Mostrar título
st.title("Lectura de registro_analisis.csv")
st.header("Búsqueda recursiva del archivo desde la raíz")

# Buscar el archivo
archivo_encontrado = buscar_archivo_recursivamente(DIRECTORIO_RAIZ, ARCHIVO_OBJETIVO)

# Mostrar resultados
if archivo_encontrado:
    st.success(f"Archivo encontrado en: {archivo_encontrado}")

    # Mostrar contenido del archivo
    try:
        st.header("Contenido del archivo")
        df = pd.read_csv(archivo_encontrado)
        st.dataframe(df)
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
    
    # Descargar el archivo
    st.header("Descargar archivo")
    with open(archivo_encontrado, "rb") as file:
        st.download_button(
            label=f"Descargar {ARCHIVO_OBJETIVO}",
            data=file,
            file_name=ARCHIVO_OBJETIVO,
            mime="text/csv"
        )
else:
    st.error(f"No se encontró el archivo {ARCHIVO_OBJETIVO} en la ruta {DIRECTORIO_RAIZ}.")

