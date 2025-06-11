import streamlit as st
from components.document_data_management import clean_document, getDataFromDocument, download_full_document, split_and_download_zip
from components.multiselect_component import multiselectFunction

st.title("Formato de documentos")

uploaded_file = st.file_uploader("Sube un archivo xlxs", type=["xlsx"])

if uploaded_file is not None:
	document_data = getDataFromDocument(uploaded_file)
	
	# TODO Limitar preview de dataframe??
	st.write("Vista previa de archivo cargado:")
	st.dataframe(document_data)

	# Seleccionar columnas de referencia para encontrar duplicados
	# TODO Titulos de columnas deben ser unicamente strings (De momento no se validan otros tipos)
	selected_columns_remove_duplicates = multiselectFunction(
		label="Selecciona las columnas de referencia para encontrar duplicados",
		options=document_data,
		help="Selecciona las columnas que se utilizarán para identificar duplicados en el archivo.", 
		placeholder="Selecciona por lo menos una columna",
	)

	st.write("You selected: ", selected_columns_remove_duplicates)

	# TODO ocultar o bloquear boton despues de primer click para evitar errores o crasheos
	# document_data_cleaned = None
	if st.button("Limpiar archivo"):
		if len(selected_columns_remove_duplicates) == 0:
			st.warning("Por favor, selecciona al menos una columna.")
			document_data_cleaned = None
		else:
			document_data_cleaned = clean_document(document_data, selected_columns_remove_duplicates)

			# Si el archivo se ha limpiado correctamente, permitir dividir y comprimir
			# Es opcional dividir y comprimir el archivo)
			# TODO Corregir, se borran botones despues de modificar numero o dato, debe quedarse activo hasta que se descargue archivo

			download_full_document(document_data_cleaned, uploaded_file)

			max_rows = st.number_input("Número de filas por archivo", min_value=10)
			if max_rows >= 1:
				split_and_download_zip(document_data_cleaned, uploaded_file, max_rows)

	else:
		st.error("El archivo no se ha limpiado correctamente.")	

else:
	st.warning("Por favor, sube un archivo Excel para comenzar.")
	st.info("El archivo debe estar en formato .xlsx")

