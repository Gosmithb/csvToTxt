import streamlit as st

# Componente de multiselect personalizado para Streamlit
# Options debe ser ['', ''] o un DataFrame de pandas
def multiselectFunction(label: str, options, default = None, help: str = "", placeholder: str = "", accept_new_options: bool = False, key: str = "ref_columns"):
  return st.multiselect(
    label=label,
    options=options.columns.tolist(),
    default=None,
    help=help, 
    placeholder=placeholder,
    accept_new_options=accept_new_options,
    key=key
  )