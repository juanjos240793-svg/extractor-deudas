import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Analizador de Deudas", page_icon="💰")

# Configuración de la API Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configura la clave en los Secrets de Streamlit.")
    st.stop()

# Usamos el nombre de modelo más compatible
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📄 Extractor de Acuerdos de Pago")
st.markdown("Sube la imagen para generar el texto de regularización.")

uploaded_file = st.file_uploader("Selecciona la imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen cargada", use_container_width=True)

    if st.button("Generar Texto"):
        with st.spinner("Analizando información con IA..."):
            prompt = """
            Lee la tabla de la imagen y genera un texto con este formato exacto:

            Monto total deuda: [Monto total]
            Dias total deuda: [Dias total]

            Esposible regularizar: 

            🟡 Opción 1 – Liquidación con beneficio
            Se le ofrece la oportunidad de liquidar su adeudo con descuento en intereses.
            Realizando el pago el día de hoy, podrá saldar su deuda por un monto preferencial de 💳 [Monto con descuento]

            🟡 Opción 2 – Refinanciamiento. En caso de requerir un esquema de pago, el refinanciamiento se realiza por 

            [Listar todas las cuotas: X cuotas fijas de $ Y]

            Esperamos su confirmacion
            """
            try:
                # Llamada simplificada para evitar errores de versión
                response = model.generate_content([prompt, img])
                st.subheader("Resultado:")
                st.text_area("Copia el texto aquí:", value=response.text, height=350)
            except Exception as e:
                st.error(f"Error: {e}")


