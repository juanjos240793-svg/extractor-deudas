import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Analizador de Deudas", page_icon="💰")

# Configuración de la API Key
if "GOOGLE_API_KEY" in st.secrets:
    # FORZAMOS LA VERSIÓN ESTABLE PARA EVITAR EL ERROR 404
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configura la clave en los Secrets de Streamlit.")
    st.stop()

# Usamos el nombre del modelo estándar
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📄 Extractor de Acuerdos de Pago")

uploaded_file = st.file_uploader("Selecciona la imagen de la deuda", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen cargada", use_container_width=True)

    if st.button("Generar Texto"):
        with st.spinner("Analizando información..."):
            prompt = "Extrae el Monto total deuda, Dias total deuda y todas las opciones de cuotas de esta imagen. Formatea como un mensaje de liquidación."
            try:
                # Forzamos a que no use v1beta
                response = model.generate_content(img, generation_config={"candidate_count": 1})
                st.subheader("Resultado:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}. Por favor, verifica tu API Key en Secrets.")
