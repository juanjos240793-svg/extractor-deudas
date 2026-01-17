import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Extractor de Deudas", page_icon="💰")

# Configuración de la API Key
if "GOOGLE_API_KEY" in st.secrets:
    # FORZAMOS LA API A USAR LA VERSIÓN ESTABLE v1
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
    st.stop()

st.title("📄 Extractor de Acuerdos de Pago")

archivo = st.file_uploader("Sube la imagen de la deuda", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Imagen cargada correctamente")

    if st.button("Generar Texto"):
        with st.spinner("Analizando información..."):
            try:
                # CAMBIO CRÍTICO: Usamos el modelo con el nombre técnico de producción
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                prompt = "Extrae el Monto total deuda, Dias total deuda y las opciones de cuotas de esta imagen."
                
                # Forzamos la respuesta
                response = model.generate_content([prompt, img])
                
                st.success("¡Análisis completado!")
                st.write(response.text)
            except Exception as e:
                # Si esto falla, intentamos una ruta alternativa automática
                st.error(f"Error detectado: {e}. Reintentando con configuración de respaldo...")
                model_alt = genai.GenerativeModel('gemini-1.5-flash')
                response = model_alt.generate_content([prompt, img])
                st.write(response.text)
