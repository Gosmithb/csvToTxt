import streamlit as st
import time
import numpy as np


st.title("Formato de documentos")

uploaded_file = st.file_uploader("Sube un archivo xlxs", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Datos cargados:")
    st.dataframe(df)

    # Simulación de procesamiento
    with st.spinner("Procesando..."):
        time.sleep(2)  # Simula un tiempo de procesamiento

    st.success("Archivo procesado correctamente")
    
    # Aquí podrías agregar más lógica para formatear el documento según tus necesidades