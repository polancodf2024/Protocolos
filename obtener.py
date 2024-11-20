import streamlit as st
from pathlib import Path

# Obtener el directorio actual
directorio_actual = Path.cwd()

# Subir al nivel padre para explorar directorios hermanos
nivel_superior = directorio_actual.parent

# Mostrar directorios disponibles
st.title("Depuración de Rutas y Búsqueda de Archivo")
st.header("Exploración de Directorios")

st.write("Directorio actual:", directorio_actual)
st.write("Nivel superior (padre):", nivel_superior)

# Listar subdirectorios en el nivel superior
st.header("Directorios en el nivel superior")
for carpeta in nivel_superior.iterdir():
    if carpeta.is_dir():
        st.write(f"Directorio encontrado: {carpeta}")

# Intentar buscar el archivo en el directorio 'analisisestadistico'
RUTA_ANALISIS = nivel_superior / "analisisestadistico"
ARCHIVO_OBJETIVO = "registro_analisis.csv"

st.header("Búsqueda en 'analisisestadistico'")
if RUTA_ANALISIS.exists():
    archivo_path = RUTA_ANALISIS / ARCHIVO_OBJETIVO
    if archivo_path.exists():
        st.success(f"Archivo encontrado en: {archivo_path}")
    else:
        st.error(f"No se encontró el archivo {ARCHIVO_OBJETIVO} en el directorio {RUTA_ANALISIS}")
else:
    st.error(f"El directorio 'analisisestadistico' no existe en {nivel_superior}")

