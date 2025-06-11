import io
import math
import zipfile
import streamlit as st
import pandas as pd

@st.cache_data
def convert_for_download(df):
	return df.to_csv().encode("utf-8")

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
			
			document_data_without_empty_rows = document_data.dropna(subset=valid_columns)
			document_data_cleaned = document_data_without_empty_rows.drop_duplicates(subset=valid_columns)
	
			st.write("Archivo sin duplicados:")
			st.dataframe(document_data_cleaned)

			st.success("¡Proceso finalizado!")
			return document_data_cleaned
		
def split_and_zip_document_csv(max_rows, document_data_cleaned):
	number_of_files = math.ceil(len(document_data_cleaned) / max_rows)
	zip_buffer = io.BytesIO()

	with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
		for i in range(number_of_files):
			start = i * max_rows
			end = start + max_rows
			documento_section = document_data_cleaned.iloc[start:end]

			# Guardar cada sección como un archivo CSV en memoria
			csv_buffer = io.StringIO()
			documento_section.to_csv(csv_buffer, index=False)
			csv_data = csv_buffer.getvalue()

			# Generar nombre válido para el archivo CSV
			file_name = f"parte_{i+1}.csv"
			valid_file_name = "".join(c if c.isalnum() or c in ('_', '.') else '_' for c in file_name)
			valid_file_name = valid_file_name[:255]

			# Agregar al ZIP
			zip_file.writestr(valid_file_name, csv_data)

	zip_buffer.seek(0)

	return zip_buffer

def download_full_document(document_data_cleaned, uploaded_file):
	document_data_cleaned_csv = convert_for_download(document_data_cleaned)
	st.download_button(
		label="Descargar como CSV",
		data=document_data_cleaned_csv,
		file_name=f"{uploaded_file.name}_limpio.csv",
		mime="text/csv",
		icon=":material/download:",
	)

def split_and_download_zip(document_data_cleaned, uploaded_file, max_rows):
	if max_rows <= 0:
		st.error("El número máximo de filas debe ser mayor que cero.")
	else:
		generated_zip = split_and_zip_document_csv(max_rows, document_data_cleaned)
		st.download_button(
			"Descargar ZIP",
			data=generated_zip,
			file_name=f"{uploaded_file.name}_limpio.zip",
			mime="application/zip"
		)
				


