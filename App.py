import streamlit as st
import pandas as pd

def main():
  st.set_page_config(
    page_title="Proyecto CSV",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="collapsed"
  )

  st.sidebar.success("Selecciona una página del menú")
  st.title("Proyecto CSV")
  st.write("Este proyecto permite cargar un archivo CSV y recibir el resultado con formato deseado")
  st.write("Selecciona en el menú de la izquierda una de las opciones disponibles")

if __name__ == "__main__":
  main()
