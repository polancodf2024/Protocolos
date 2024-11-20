import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración
RUTA_ESPECIFICA = Path("/mount/src/analisisestadistico/")
ARCHIVO_OBJETIVO = "registro_analisis.csv"

# Verificar si el archivo está en la ruta específica
st.title("Lectura de registro_analisis.csv")
st.header("Búsqueda en ruta específica")

archivo_encontrado = None
if RUTA_ESPECIFICA.exists():
    archivo_path = RUTA_ESPECIFICA / ARCHIVO_OBJETIVO
    if archivo_path.exists():
        archivo_encontrado = archivo_path
        st.success(f"Archivo encontrado en: {archivo_encontrado}")
    else:
        st.error(f"No se encontró el archivo {ARCHIVO_OBJETIVO} en la ruta {RUTA_ESPECIFICA}")
else:
    st.error(f"La ruta {RUTA_ESPECIFICA} no existe.")

# Mostrar contenido del archivo si se encontró
if archivo_encontrado:
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

