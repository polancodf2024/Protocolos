import streamlit as st
from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime
import pytz
import csv
import os

# Configuración
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"
NOTIFICATION_EMAIL = "polanco@unam.mx"
LOG_FILE = "transaction_log.xlsx"
CSV_FILE = "registro_protocolos.csv"
MAX_FILE_SIZE_MB = 20

# Selección de idioma
idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"], index=0)

# Función para registrar transacciones en Excel
def log_transaction(nombre, email, file_name, servicios):
    tz_mexico = pytz.timezone("America/Mexico_City")
    fecha_hora = datetime.now(tz_mexico).strftime("%Y-%m-%d %H:%M:%S")
    data = {"Nombre": [nombre], "Email": [email], "Fecha y Hora": [fecha_hora], "Archivo": [file_name], "Servicios": [", ".join(servicios)]}
    df = pd.DataFrame(data)

    if not Path(LOG_FILE).exists():
        df.to_excel(LOG_FILE, index=False)
    else:
        existing_df = pd.read_excel(LOG_FILE)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(LOG_FILE, index=False)

# Función para registrar transacciones en CSV
def guardar_solicitud_csv(nombre, email, numero_economico, file_name, servicios):
    tz_mexico = pytz.timezone("America/Mexico_City")
    fecha_hora = datetime.now(tz_mexico).strftime("%Y-%m-%d %H:%M:%S")
    servicios_str = ", ".join(servicios)

    encabezados = ["Fecha y Hora", "Nombre", "Correo Electrónico", "Número Económico", "Nombre del Archivo", "Servicios Solicitados"]
    datos = [fecha_hora, nombre, email, numero_economico, file_name, servicios_str]

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(encabezados)
            writer.writerow(datos)
    except Exception as e:
        st.error(f"Error al guardar la solicitud en CSV: {e}")

# Función para enviar confirmación al usuario
def send_confirmation(email, nombre, servicios, idioma):
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = email
        mensaje['Subject'] = "Confirmación de recepción" if idioma == "Español" else "Receipt Confirmation"
        cuerpo = f"Hola {nombre}, hemos recibido tu archivo. Servicios solicitados: {', '.join(servicios)}." if idioma == "Español" else f"Hello {nombre}, we have received your file. Requested services: {', '.join(servicios)}."
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, email, mensaje.as_string())
    except Exception as e:
        st.error(f"Error al enviar confirmación al usuario: {e}")

# Función para enviar el archivo y detalles al administrador
def send_to_admin(file_data, file_name, nombre, email, numero_economico, servicios):
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = NOTIFICATION_EMAIL
        mensaje['Subject'] = "Nuevo documento recibido"

        cuerpo = (
            f"Se ha recibido un nuevo documento.\n\n"
            f"Nombre del usuario: {nombre}\n"
            f"Correo electrónico del usuario: {email}\n"
            f"Número económico: {numero_economico}\n"
            f"Servicios solicitados: {', '.join(servicios)}\n"
        )
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Adjuntar archivo subido por el usuario
        part_user_file = MIMEBase("application", "octet-stream")
        part_user_file.set_payload(file_data)
        encoders.encode_base64(part_user_file)
        part_user_file.add_header("Content-Disposition", f"attachment; filename={file_name}")
        mensaje.attach(part_user_file)

        # Adjuntar el archivo de registro CSV
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "rb") as csv_file:
                part_csv_file = MIMEBase("application", "octet-stream")
                part_csv_file.set_payload(csv_file.read())
                encoders.encode_base64(part_csv_file)
                part_csv_file.add_header("Content-Disposition", "attachment; filename=registro_protocolos.csv")
                mensaje.attach(part_csv_file)
        else:
            st.warning("El archivo 'registro_protocolos.csv' no existe aún. No se adjuntará.")

        # Enviar correo
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, NOTIFICATION_EMAIL, mensaje.as_string())

    except Exception as e:
        st.error(f"Error al enviar el correo al administrador: {e}")

# Interfaz de Streamlit
st.image("escudo_COLOR.jpg", width=100)
st.title("Revisión de Protocolos" if idioma == "Español" else "Protocol Review")

# Solicitar información del usuario
nombre_completo = st.text_input("Nombre completo")
email = st.text_input("Correo electrónico")
email_confirmacion = st.text_input("Confirma tu correo")
numero_economico = st.text_input("Número económico")

# Selección de servicios
servicios_solicitados = st.multiselect(
    "¿Qué servicios solicita?",
    ["Revisión Ética y Bioética", "Evaluar calidad metodológica", "Asesoría en cumplimiento de riesgos", "Soporte en gestión de datos"]
)

# Subida de archivo
uploaded_file = st.file_uploader("Sube tu archivo (.doc, .docx)", type=["doc", "docx"])

# Procesar envío
if st.button("Enviar archivo"):
    if not nombre_completo or not email or not email_confirmacion or not numero_economico or uploaded_file is None or not servicios_solicitados:
        st.error("Por favor, completa todos los campos.")
    elif email != email_confirmacion:
        st.error("Los correos electrónicos no coinciden.")
    else:
        with st.spinner("Enviando..."):
            file_data = uploaded_file.getbuffer()
            file_name = uploaded_file.name

            log_transaction(nombre_completo, email, file_name, servicios_solicitados)
            guardar_solicitud_csv(nombre_completo, email, numero_economico, file_name, servicios_solicitados)
            send_confirmation(email, nombre_completo, servicios_solicitados, idioma)
            send_to_admin(file_data, file_name, nombre_completo, email, numero_economico, servicios_solicitados)

            st.success("Envío exitoso. Puedes cerrar la aplicación.")

