import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestor Nube Pro", page_icon="☁️")

# URL de tu hoja (PEGA TU LINK AQUÍ ABAJO)
URL_HOJA = "https://docs.google.com/spreadsheets/d/TU_ID_AQUI/edit?usp=sharing".strip()

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📈 Control de Negocio (Nube)")

# --- FORMULARIO DE REGISTRO ---
with st.form(key="ventas_form"):
    tipo = st.selectbox("Categoría", ["Venta (Ingreso)", "Gasto (Salida)"])
    concepto = st.text_input("Descripción")
    monto = st.number_input("Monto (RD$)", min_value=0.0, step=50.0)
    fecha = st.date_input("Fecha", datetime.now())
    
    boton_enviar = st.form_submit_button("Guardar en la Nube")

if boton_enviar:
    if concepto and monto > 0:
        # 1. Leer datos existentes de la hoja
        df_actual = conn.read(spreadsheet=URL_HOJA)
        
        # 2. Crear la nueva fila de datos
        nueva_data = pd.DataFrame([{
            "tipo": tipo,
            "concepto": concepto,
            "monto": monto,
            "fecha": str(fecha)
        }])
        
        # 3. Combinar y subir de nuevo
        df_final = pd.concat([df_actual, nueva_data], ignore_index=True)
        conn.update(spreadsheet=URL_HOJA, data=df_final)
        
        st.success("✅ ¡Datos guardados permanentemente!")
        st.balloons()
    else:
        st.error("⚠️ Por favor rellena todos los campos.")

# --- VISUALIZACIÓN DE DATOS ---
st.divider()
st.subheader("📋 Historial desde Google Sheets")
df_nube = conn.read(spreadsheet=URL_HOJA)
st.dataframe(df_nube, use_container_width=True)
