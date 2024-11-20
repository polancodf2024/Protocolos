import streamlit as st
import os
from pathlib import Path
import pandas as pd
import subprocess

# Configuración del archivo CSV
CSV_FILE = "registro_protocolos.csv"

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

# Función para inicializar configuración de Git
def inicializar_git():
    try:
        # Configurar nombre y correo si es necesario
        subprocess.run(["git", "config", "--global", "user.name", "Streamlit User"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "streamlit@example.com"], check=True)
    except Exception as e:
        st.error("Error al configurar Git. Verifica los permisos y el entorno.")
        st.error(str(e))

# Función para actualizar el archivo en GitHub
def actualizar_en_github(archivo):
    try:
        # Inicializar Git si no está configurado
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/polancodf2024/PROTOCOLOS.git"], check=True)
        
        # Agregar el archivo a Git
        subprocess.run(["git", "add", archivo], check=True)
        
        # Realizar un commit
        subprocess.run(["git", "commit", "-m", "Actualización del archivo registro_protocolos.csv"], check=True)
        
        # Hacer push al repositorio remoto
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        st.success("Archivo actualizado en GitHub exitosamente.")
    except subprocess.CalledProcessError as e:
        st.error("Error al intentar actualizar el archivo en GitHub.")
        st.error(f"Comando: {e.cmd}")
        st.error(f"Salida: {e.output}")
    except Exception as e:
        st.error("Error inesperado.")
        st.error(str(e))

# Llama a la inicialización antes de actualizar GitHub
inicializar_git()

# Opción para subir el archivo registro_protocolos.csv
st.header("Subir el archivo registro_protocolos.csv")
uploaded_csv = st.file_uploader("Selecciona el archivo para subir y reemplazar el existente", type=["csv"])

if uploaded_csv is not None:
    try:
        # Guardar el archivo subido temporalmente
        temp_file = "temp_protocolos.csv"
        with open(temp_file, "wb") as f:
            f.write(uploaded_csv.getbuffer())

        # Reemplazar el archivo existente
        os.system(f"cp {temp_file} {CSV_FILE}")
        st.success("Archivo registro_protocolos.csv subido y reemplazado exitosamente.")

        # Actualizar en GitHub
        actualizar_en_github(CSV_FILE)

        # Mostrar una vista previa del archivo subido
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)

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

