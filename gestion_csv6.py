import streamlit as st
import os
from pathlib import Path
import pandas as pd
import base64
import requests

# Configuración del archivo CSV y GitHub
CSV_FILE = "registro_protocolos.csv"
GITHUB_REPO = "polancodf2024/protocolos"
GITHUB_TOKEN = "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"  # Reemplaza esto con tu token válido
GITHUB_FILE_PATH = "registro_protocolos.csv"  # Ruta en el repositorio GitHub

# Solicitar contraseña al inicio
PASSWORD = "Tt5plco5"
input_password = st.text_input("Ingresa la contraseña para acceder:", type="password")

# Verificar la contraseña
if input_password != PASSWORD:
    st.error("Contraseña incorrecta. No tienes acceso a esta página.")
    st.stop()

# Mostrar el logo del escudo
st.image("escudo_COLOR.jpg", width=150)

# Título de la aplicación
st.title("Gestión de Archivo: registro_protocolos.csv")

# Función para subir el archivo a GitHub
def subir_a_github(file_path, file_content):
    try:
        # Verificar si el archivo ya existe en el repositorio
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # El archivo ya existe, necesitamos su SHA para actualizarlo
            sha = response.json()["sha"]
            data = {
                "message": "Actualización del archivo registro_protocolos.csv desde Streamlit",
                "content": base64.b64encode(file_content.encode()).decode(),
                "sha": sha
            }
        else:
            # El archivo no existe, lo crearemos
            data = {
                "message": "Creación del archivo registro_protocolos.csv desde Streamlit",
                "content": base64.b64encode(file_content.encode()).decode()
            }

        # Subir el archivo a GitHub
        response = requests.put(url, headers=headers, json=data)

        st.write(f"URL: {url}")
        st.write(f"Headers: {headers}")
        st.write(f"Data: {data}")
        st.write(f"Response status: {response.status_code}")
        st.write(f"Response content: {response.content}")

        if response.status_code in [200, 201]:
            st.success("Archivo actualizado en GitHub exitosamente.")
        else:
            st.error(f"Error al subir el archivo a GitHub: {response.status_code}")
            st.error(response.json())

    except Exception as e:
        st.error("Error al conectar con GitHub.")
        st.error(str(e))

# Opción para subir el archivo registro_protocolos.csv
st.header("Subir el archivo registro_protocolos.csv")
uploaded_csv = st.file_uploader("Selecciona el archivo para subir y reemplazar el existente", type=["csv"])

if uploaded_csv is not None:
    try:
        # Guardar el archivo subido temporalmente
        temp_file = "temp_protocolos.csv"
        with open(temp_file, "wb") as f:
            f.write(uploaded_csv.getbuffer())

        # Reemplazar el archivo existente localmente
        os.system(f"cp {temp_file} {CSV_FILE}")
        st.success("Archivo registro_protocolos.csv subido y reemplazado exitosamente.")

        # Mostrar una vista previa del archivo subido
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)

        # Leer el contenido del archivo para GitHub
        with open(CSV_FILE, "r") as file:
            file_content = file.read()

        # Subir el archivo a GitHub
        subir_a_github(GITHUB_FILE_PATH, file_content)

        # Eliminar el archivo temporal
        os.remove(temp_file)

    except Exception as e:
        st.error("Error al subir el archivo. Por favor, intenta nuevamente.")
        st.error(str(e))

# Opción para descargar el archivo registro_protocolos.csv
st.header("Descargar el archivo registro_protocolos.csv")

if Path(CSV_FILE).exists():
    try:
        with open(CSV_FILE, "rb") as file:
            st.download_button(
                label="Descargar registro_protocolos.csv",
                data=file,
                file_name="registro_protocolos.csv",
                mime="text/csv"
            )
        st.success("Archivo listo para descargar.")
    except Exception as e:
        st.error("Error al descargar el archivo.")
        st.error(str(e))
else:
    st.warning("El archivo registro_protocolos.csv no existe.")

