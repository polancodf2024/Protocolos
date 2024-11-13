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

# Configuración
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"
NOTIFICATION_EMAIL = "polanco@unam.mx"
LOG_FILE = "transaction_log.xlsx"
MAX_FILE_SIZE_MB = 20

# Selección de idioma
idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"], index=0)

# Función para registrar transacciones
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

# Función para enviar confirmación
def send_confirmation(email, nombre, servicios, idioma):
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

# Añadir logo y título
st.image("escudo_COLOR.jpg", width=100)
st.title("Unidad de Revisión de Protocolos" if idioma == "Español" else "Protocol Review Center")

# Solicitar información del usuario
nombre_completo = st.text_input("Nombre completo" if idioma == "Español" else "Full name")
email = st.text_input("Correo electrónico" if idioma == "Español" else "Email")
email_confirmacion = st.text_input("Confirma tu correo" if idioma == "Español" else "Confirm your email")

# Selección de servicios
servicios_solicitados = st.multiselect(
    "¿Qué servicios solicita?" if idioma == "Español" else "What services do you require?",
    ["Evaluar calidad metodológica", "Revisión Ética y Bioética", "Revisión del consentimiento informado", "Revisión de cumplimiento legal y contractual", "Asesoría en cumplimiento de riesgos", "Soporte en gestión de datos", "Asistencia en procedimientos"] if idioma == "Español" else ["Methodological quality", "Ethical review", "Informed consent review", "Legal compliance", "Risk advisory", "Data management support", "Approval procedures"]
)


# Subida de archivo
st.error("Sube tu archivo (.doc, .docx). Nota: el tamaño máximo es 20 MB, no 200 MB" if idioma == "Español" else "Upload your file (.doc, .docx). Note: the maximum file size is 20 MB, not 200 MB")

uploaded_file = st.file_uploader(
    "Sube tu archivo (.doc, .docx)" if idioma == "Español" else "Upload your file (.doc, .docx)",
    type=["doc", "docx"],
    label_visibility="collapsed"
)

# Enviar archivo y registro
if st.button("Enviar archivo" if idioma == "Español" else "Submit file"):
    if not nombre_completo:
        st.error("Ingresa tu nombre." if idioma == "Español" else "Enter your name.")
    elif not email or not email_confirmacion:
        st.error("Confirma tu correo." if idioma == "Español" else "Confirm your email.")
    elif email != email_confirmacion:
        st.error("Los correos no coinciden." if idioma == "Español" else "Emails do not match.")
    elif uploaded_file is None:
        st.error("Adjunta un archivo." if idioma == "Español" else "Attach a file.")
    elif len(uploaded_file.getbuffer()) > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"Archivo muy grande (máx {MAX_FILE_SIZE_MB} MB)." if idioma == "Español" else f"File too large (max {MAX_FILE_SIZE_MB} MB).")
    elif not servicios_solicitados:
        st.error("Selecciona un servicio." if idioma == "Español" else "Select a service.")
    else:
        with st.spinner("Enviando..."):
            file_data = uploaded_file.getbuffer()
            file_name = uploaded_file.name
            log_transaction(nombre_completo, email, file_name, servicios_solicitados)
            send_confirmation(email, nombre_completo, servicios_solicitados, idioma)
            st.success("Envío exitoso." if idioma == "Español" else "Submission successful.")


