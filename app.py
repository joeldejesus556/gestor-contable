import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor Joel Pro", page_icon="📈")

# --- CONFIGURACIÓN ---
ID_HOJA = "1So7au1zmTk5KQOjh2MKGO41CL4WmYoJMAcCrguj15RI" 
URL_CSV = f"https://docs.google.com/spreadsheets/d/{ID_HOJA}/export?format=csv"
URL_FORM = "https://forms.gle/tHHCXYrAu7TVqBhE8"

st.title("🚀 Sistema de Control Digital")
st.info("Ingeniería de Software - Dashboard de Finanzas")

# --- SECCIÓN DE REGISTRO ---
st.subheader("➕ Registrar Venta o Gasto")
st.link_button("📝 Abrir Formulario de Registro", URL_FORM, use_container_width=True)

st.divider()

# --- SECCIÓN DE CÁLCULOS Y VISUALIZACIÓN ---
try:
    df = pd.read_csv(URL_CSV)
    
    if not df.empty:
        # 1. Limpieza de datos (Aseguramos que 'Monto' sea número)
        # Nota: Asegúrate que en tu Excel la columna se llame exactamente 'Monto'
        df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
        
        # 2. Cálculos Lógicos
        # Filtramos por la columna 'Tipo' (Asegúrate que se llame así en tu Excel)
        ingresos = df[df['Tipo'].str.contains("Ingreso", na=False)]['Monto'].sum()
        gastos = df[df['Tipo'].str.contains("Gasto", na=False)]['Monto'].sum()
        ganancia_neta = ingresos - gastos

        # 3. Mostrar Métricas (Tablero)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"RD$ {ingresos:,.2f}")
        col2.metric("Total Gastos", f"RD$ {gastos:,.2f}", delta=f"-{gastos:,.2f}", delta_color="inverse")
        col3.metric("Ganancia Neta", f"RD$ {ganancia_neta:,.2f}")

        st.subheader("📋 Historial Detallado")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.warning("Aún no hay registros en la base de datos.")
except Exception as e:
    st.error("Error al cargar datos. Revisa que los nombres de las columnas en Excel sean 'Tipo' y 'Monto'.")
    # st.write(e) # Descomenta esta línea si quieres ver el error específico
