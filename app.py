import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Extractor de Deudas", page_icon="💰")

# Configuración de la API Key desde los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
    st.stop()

# Título de la App
st.title("📄 Extractor de Acuerdos de Pago")

archivo = st.file_uploader("Sube la imagen de la deuda", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Imagen cargada correctamente")

    if st.button("Generar Texto"):
        with st.spinner("Analizando información con IA..."):
            try:
                # Usamos el modelo más estable y rápido
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Pedimos los datos específicos de tu tabla
                prompt = "Extrae de la imagen: Monto total deuda, Dias total deuda y los montos de las cuotas."
                
                response = model.generate_content([prompt, img])
                
                st.success("¡Análisis completado!")
                st.text_area("Copia el resultado:", value=response.text, height=300)
            except Exception as e:
                st.error(f"Error técnico: {e}")
