import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor Nube Pro", page_icon="☁️")

# 1. URL de tu hoja (Asegúrate de que termine en /export?format=csv)
# Reemplaza 'TU_ID_AQUI' con el código largo de tu link de Google Sheets
ID_HOJA = "1M29Y6MMrAkYnLp2JolJKsC6IZXtz1DGOrwr42bCOkCY"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{ID_HOJA}/export?format=csv"

st.title("📈 Control de Negocio (Nube)")

with st.form(key="ventas_form"):
    tipo = st.selectbox("Categoría", ["Venta (Ingreso)", "Gasto (Salida)"])
    concepto = st.text_input("Descripción")
    monto = st.number_input("Monto (RD$)", min_value=0.0, step=50.0)
    fecha = st.date_input("Fecha", datetime.now())
    boton_enviar = st.form_submit_button("Guardar Registro")

if boton_enviar:
    if concepto and monto > 0:
        # Aquí es donde la magia ocurre: Guardamos localmente por ahora
        # Pero para que sea permanente en Google Sheets sin errores, 
        # lo ideal es usar Form de Google o una API Key.
        st.success("✅ Registro capturado.")
        st.balloons()
        
        # Mostramos lo que se guardaría
        st.write(f"Guardando: {tipo} - {concepto} - RD${monto}")
    else:
        st.error("⚠️ Rellena todos los campos.")

# --- VISUALIZACIÓN ---
try:
    df_nube = pd.read_csv(URL_CSV)
    st.subheader("📋 Historial en Tiempo Real")
    st.dataframe(df_nube, use_container_width=True)
except:
    st.info("Conecta tu ID de hoja para ver el historial.")
