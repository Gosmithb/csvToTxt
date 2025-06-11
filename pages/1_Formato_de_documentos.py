import streamlit as st
import pandas as pd
from components.document_data_managment import clean_document, getDataFromDocument

st.title("Formato de documentos")

uploaded_file = st.file_uploader("Sube un archivo xlxs", type=["xlsx"])

if uploaded_file is not None:
    document_data = getDataFromDocument(uploaded_file)
    
    st.write("Vista previa de archivo cargado:")
    st.dataframe(document_data)

    # Seleccionar columnas de referencia para encontrar duplicados
    # TODO Titulos de columnas deben ser unicamente strings (De momento no se validan otros tipos)
    selected_columns_remove_duplicates = st.multiselect(
        "Selecciona las columnas de referencia para encontrar duplicados",
        options=document_data.columns.tolist(),
        default=None,
        help="Selecciona las columnas que se utilizarán para identificar duplicados en el archivo.", 
        placeholder="Selecciona por lo menos una columna",
        accept_new_options=False,
        key="ref_columns"
    )

    st.write("You selected: ", selected_columns_remove_duplicates)

    # TODO ocultar o bloquear boton despues de primer click para evitar errores o crasheos
    if st.button("Limpiar archivo"):
        if len(selected_columns_remove_duplicates) == 0:
            st.warning("Por favor, selecciona al menos una columna para eliminar duplicados.")
        else:
            clean_document(document_data, selected_columns_remove_duplicates)



    # # Simulación de procesamiento
    # with st.spinner("Procesando..."):
    #     time.sleep(2)  # Simula un tiempo de procesamiento

    # st.success("Archivo procesado correctamente")
    
    # Aquí podrías agregar más lógica para formatear el documento según tus necesidades
else:
    st.warning("Por favor, sube un archivo Excel para comenzar.")
    st.info("El archivo debe estar en formato .xlsx")

