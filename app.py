import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración visual de la página
st.set_page_config(page_title="Analizador de Deudas", page_icon="💰")

# 1. Conectar con la API Key (configurada en Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los Secrets de Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-pro-vision')

st.title("📄 Extractor de Acuerdos de Pago")
st.markdown("Sube la imagen para generar el texto de regularización automáticamente.")

# 2. Subida de la imagen
uploaded_file = st.file_uploader("Selecciona la imagen de la deuda", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen cargada", use_container_width=True)

    if st.button("Generar Texto"):
        with st.spinner("Analizando información..."):
            # Instrucción detallada para la IA
            prompt = """
            Analiza la imagen de la tabla de deuda. 
            Extrae los datos y redacta el siguiente mensaje exacto:

            Monto total deuda: [Monto total de la deuda]
            Dias total deuda: [Días totales]

            Esposible regularizar: 

            🟡 Opción 1 – Liquidación con beneficio
            Se le ofrece la oportunidad de liquidar su adeudo con descuento en intereses.
            Realizando el pago el día de hoy, podrá saldar su deuda por un monto preferencial de 💳 [Monto de la fila que tiene descuento]

            🟡 Opción 2 – Refinanciamiento. En caso de requerir un esquema de pago, el refinanciamiento se realiza por 

            [Listar todas las filas de cuotas disponibles en la tabla con este formato: X cuotas fijas de $ Y.YYY,YY]

            Esperamos su confirmacion
            """
            
            try:
                # La IA procesa la imagen y el texto
                response = model.generate_content([prompt, img])
                
                st.subheader("Resultado para copiar:")
                st.text_area("Texto listo:", value=response.text, height=350)
                st.success("¡Listo! Ya puedes copiar el texto.")
            except Exception as e:
                st.error(f"Error al procesar la imagen: {e}")

