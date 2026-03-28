import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor Nube Pro", page_icon="☁️")

# Conexión profesional (usará los Secrets de Streamlit)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📈 Control de Negocio (Nube)")

with st.form(key="ventas_form"):
    tipo = st.selectbox("Categoría", ["Venta (Ingreso)", "Gasto (Salida)"])
    concepto = st.text_input("Descripción")
    monto = st.number_input("Monto (RD$)", min_value=0.0, step=50.0)
    fecha = st.date_input("Fecha", datetime.now())
    boton_enviar = st.form_submit_button("Guardar en la Nube")

if boton_enviar:
    if concepto and monto > 0:
        # Leer y actualizar de la hoja configurada en Secrets
        df_actual = conn.read() 
        nueva_data = pd.DataFrame([{"tipo": tipo, "concepto": concepto, "monto": monto, "fecha": str(fecha)}])
        df_final = pd.concat([df_actual, nueva_data], ignore_index=True)
        conn.update(data=df_final)
        st.success("✅ ¡Datos guardados permanentemente!")
        st.balloons()
