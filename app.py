import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Extractor de Deudas", page_icon="💰")

# Configuración de la API Key
if "GOOGLE_API_KEY" in st.secrets:
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
                # CAMBIO CLAVE: Usamos el nombre de modelo de producción
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                prompt = "Lee la tabla y dime el Monto total deuda, Dias total deuda y las cuotas."
                
                # Intentamos la llamada más básica posible
                response = model.generate_content([prompt, img])
                
                st.success("¡Análisis completado!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")

