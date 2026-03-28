import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor Joel Pro", page_icon="📈")

# --- CONFIGURACIÓN (PEGA TUS LINKS AQUÍ) ---
# 1. El link de tu HOJA (Asegúrate de que termine en /export?format=csv)
ID_HOJA = "1So7au1zmTk5KQOjh2MKGO41CL4WmYoJMAcCrguj15RI" 
URL_CSV = f"https://docs.google.com/spreadsheets/d/{ID_HOJA}/export?format=csv"

# 2. El link de tu FORMULARIO
URL_FORM = "https://forms.gle/tHHCXYrAu7TVqBhE8"

st.title("🚀 Sistema de Control Digital")
st.info("Ingeniería de Software - Proyecto Gestión")

# --- SECCIÓN DE REGISTRO ---
st.subheader("➕ Registrar Venta o Gasto")
st.write("Presiona el botón para abrir el cuaderno digital:")
st.link_button("📝 Abrir Formulario de Registro", URL_FORM, use_container_width=True)

st.divider()

# --- SECCIÓN DE VISUALIZACIÓN ---
st.subheader("📋 Historial en Tiempo Real")

try:
    # Leemos la hoja de Google Sheets
    df = pd.read_csv(URL_CSV)
    
    if not df.empty:
        # Renombramos columnas si Google les puso nombres largos
        # (Google suele poner 'Puntuación', 'Marca temporal', etc.)
        st.dataframe(df, use_container_width=True)
        
        # Un pequeño cálculo para impresionar al cliente
        # Cambia 'Monto' por el nombre exacto de tu columna en la hoja
        columnas = df.columns.tolist()
        if 'Monto' in columnas:
            total = pd.to_numeric(df['Monto'], errors='coerce').sum()
            st.metric("Flujo de Caja Total", f"RD$ {total:,.2f}")
    else:
        st.warning("Aún no hay registros. ¡Usa el formulario arriba!")
except:
    st.error("Conectando con la base de datos... Verifica que la hoja sea pública.")
