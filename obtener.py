import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración
DIRECTORIO_BUSQUEDA = Path("/mount/src/analisisestadistico/")
ARCHIVO_OBJETIVO = "registro_analisis.csv"

# Verificar si el directorio existe
st.title("Lectura de registro_analisis.csv")
st.header("Búsqueda del archivo en un directorio específico")

if DIRECTORIO_BUSQUEDA.exists():
    archivo_path = DIRECTORIO_BUSQUEDA / ARCHIVO_OBJETIVO
    if archivo_path.exists():
        st.success(f"Archivo encontrado en: {archivo_path}")

        # Mostrar contenido del archivo
        try:
            st.header("Contenido del archivo")
            df = pd.read_csv(archivo_path)
            st.dataframe(df)
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
        
        # Descargar el archivo
        st.header("Descargar archivo")
        with open(archivo_path, "rb") as file:
            st.download_button(
                label=f"Descargar {ARCHIVO_OBJETIVO}",
                data=file,
                file_name=ARCHIVO_OBJETIVO,
                mime="text/csv"
            )
    else:
        st.error(f"No se encontró el archivo {ARCHIVO_OBJETIVO} en el directorio {DIRECTORIO_BUSQUEDA}")
else:
    st.error(f"El directorio {DIRECTORIO_BUSQUEDA} no existe.")

