import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Configuración de entornos y variables secretas
# Environment and secret variables configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# Mapeo de rutas absolutas para los archivos adjuntos
# Absolute path mapping for attachments
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'Reporte_Amazon_Busqueda.xlsx')
GRAFICA_PATH = os.path.join(BASE_DIR, 'data', 'grafica_precios_amazon.png')


def enviar_reporte_automatizado():
    """
    Gestiona el protocolo SMTP para enviar el correo electrónico con los archivos de análisis adjuntos.
    Manages the SMTP protocol to send the email with the analysis files attached.
    """
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not remitente or not password:
        print("❌ [SENDER] Credenciales faltantes en el archivo .env / Missing credentials in .env file")
        return

    msg = EmailMessage()
    msg['Subject'] = '📊 Amazon Scraper Pro: Market Monitoring Report'
    msg['From'] = remitente
    msg['To'] = remitente  # Autovío / Sent to yourself

    # Plantilla de correo formal, ejecutiva y bilingüe para el usuario final
    # Formal, executive, and bilingual email template for the end-user
    cuerpo = (
        "Estimado Usuario,\n\n"
        "Se adjuntan los resultados correspondientes al monitoreo de mercado y análisis de precios automatizado.\n\n"
        "Archivos incluidos:\n"
        "1. Reporte Ejecutivo (Excel): Detalle de productos ordenados de menor a mayor costo.\n"
        "2. Análisis Estadístico (Gráfica PNG): Comparativa visual de los artículos más relevantes.\n\n"
        "--------------------------------------------------\n"
        "Dear User,\n\n"
        "Please find attached the results corresponding to the automated market monitoring and price analysis.\n\n"
        "Included files:\n"
        "1. Executive Report (Excel): Detailed list of products sorted from lowest to highest price.\n"
        "2. Statistical Analysis (PNG Chart): Visual comparison of the most relevant items.\n\n"

    )
    msg.set_content(cuerpo)

    # Definición de adjuntos con sus respectivos MIME types
    # Definitions of attachments with their respective MIME types
    adjuntos = [
        (EXCEL_PATH, 'application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
        (GRAFICA_PATH, 'image', 'png')
    ]

    for ruta, tipo, subtipo in adjuntos:
        if os.path.exists(ruta):
            with open(ruta, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype=tipo,
                    subtype=subtipo,
                    filename=os.path.basename(ruta)
                )
        else:
            print(f"⚠️ [SENDER] No se localizó el adjunto / Attachment not found at: {ruta}")

    # Conexión segura y envío a través de Gmail SMTP
    # Secure connection and dispatch via Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)
        print("🚀 [SENDER] Correo enviado exitosamente con la data fresca / Email successfully dispatched with fresh data.")
    except Exception as e:
        print(f"❌ [SENDER] Fallo en la transmisión SMTP / SMTP transmission failure: {e}")