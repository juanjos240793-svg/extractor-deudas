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

st.title("📄 Extractor de Acuerdos de Pago")

archivo = st.file_uploader("Sube la imagen de la deuda", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    st.image(img, caption="Imagen cargada correctamente")

    if st.button("Generar Texto"):
        with st.spinner("Analizando información..."):
            try:
                # FORZAMOS EL USO DE LA VERSIÓN v1 PARA EVITAR EL ERROR 404
                model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                
                prompt = """
                Analiza la tabla de la imagen y extrae exactamente estos datos:
                1. Monto total deuda
                2. Dias total deuda
                3. La lista de cuotas (Nro cuotas y Monto de la cuota)
                
                Formatea la respuesta como un mensaje de acuerdo de pago profesional.
                """
                
                # Llamada directa sin parámetros de versión que causen conflicto
                response = model.generate_content([prompt, img])
                
                st.success("¡Análisis completado!")
                st.text_area("Resultado:", value=response.text, height=350)
            except Exception as e:
                st.error(f"Error: {e}. Intenta refrescar la página.")
