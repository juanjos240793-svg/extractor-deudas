import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Extractor de Deudas", layout="centered")

# Conexión con la llave de seguridad
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
    st.stop()

# Usamos el modelo más estable
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💰 Extractor de Acuerdos de Pago")

archivo = st.file_uploader("Sube la imagen de la deuda", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Imagen cargada correctamente")

    if st.button("Generar Texto"):
        with st.spinner("Leyendo datos..."):
            # Instrucción simplificada para asegurar respuesta
            prompt = "Analiza la imagen y extrae: Monto total deuda, Dias total deuda, y las opciones de cuotas disponibles."
            
            try:
                # El cambio clave: quitamos parámetros innecesarios que causan el 404
                response = model.generate_content([prompt, img])
                
                st.success("¡Datos extraídos!")
                st.text_area("Resultado para copiar:", value=response.text, height=300)
            except Exception as e:
                st.error(f"Hubo un problema: {e}")
