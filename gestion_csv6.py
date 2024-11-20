import streamlit as st
import subprocess

st.title("Diagnóstico de Git")

try:
    # Prueba de Git
    git_version = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
    st.success("Git está instalado y funcionando.")
    st.text(git_version.stdout)

    # Verificar el remoto
    git_remote = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, check=True)
    st.text("Remotos configurados:")
    st.text(git_remote.stdout)
except subprocess.CalledProcessError as e:
    st.error("Error al ejecutar un comando de Git.")
    st.error(f"Comando: {e.cmd}")
    st.error(f"Salida: {e.stderr}")
except Exception as e:
    st.error("Error inesperado.")
    st.error(str(e))

