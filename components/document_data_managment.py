import streamlit as st
import pandas as pd

@st.cache_data
def getDataFromDocument(uploaded_file):
    # Leer el archivo Excel
    try: 
        document_data = pd.read_excel(uploaded_file)
        return document_data
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return "Archivo con formato no válido o dañado"

@st.cache_data
def clean_document(document_data, selected_columns):
    with st.spinner("Procesando..."):
        if selected_columns:
            # Eliminar duplicados basados en las columnas seleccionadas
            # Validar que las columnas seleccionadas existen y son strings
            valid_columns = [col for col in selected_columns if col in document_data.columns and isinstance(col, str)]

            if len(valid_columns) != len(selected_columns):
                st.error("Algunas columnas seleccionadas no existen o no son válidas. Por favor, verifica tu selección.")
                return None
            
            document_data_cleaned = document_data.drop_duplicates(subset=valid_columns)

            st.write("Archivo sin duplicados:")
            st.dataframe(document_data_cleaned)

            # Botón para descargar el archivo limpio
            # csv = document_data_cleaned.to_csv(index=False).encode('utf-8')
            # st.download_button(
            #     label="Descargar archivo limpio",
            #     data=csv,
            #     file_name=f"archivo_limpio_{uploaded_file.name}",
            #     mime='text/csv'
            # )

            st.success("¡Proceso finalizado!")
            return document_data_cleaned
        