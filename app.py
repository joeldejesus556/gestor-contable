import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestor de Negocio Pro", page_icon="📈")

# --- FUNCIONES DE BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect('negocio_pro.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transacciones 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  tipo TEXT, 
                  concepto TEXT, 
                  monto REAL, 
                  fecha DATE)''')
    conn.commit()
    conn.close()

init_db()

# --- INTERFAZ DE USUARIO ---
st.title("📈 Control de Ventas y Gastos")
st.markdown("---")

# Formulario para entrada de datos
with st.container():
    st.subheader("➕ Registrar Nuevo Movimiento")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        tipo = st.selectbox("Categoría", ["Venta (Ingreso)", "Gasto (Salida)"])
        concepto = st.text_input("Descripción (Ej: Corte de pelo, Pago de Luz)")
    
    with col_f2:
        monto = st.number_input("Monto (RD$)", min_value=0.0, step=50.0)
        fecha = st.date_input("Fecha del registro", datetime.now())

    if st.button("💾 Guardar en el Cuaderno Digital", use_container_width=True):
        if concepto and monto > 0:
            conn = sqlite3.connect('negocio_pro.db')
            c = conn.cursor()
            c.execute("INSERT INTO transacciones (tipo, concepto, monto, fecha) VALUES (?, ?, ?, ?)",
                      (tipo, concepto, monto, fecha))
            conn.commit()
            conn.close()
            st.success(f"✅ ¡{tipo} registrado correctamente!")
        else:
            st.error("⚠️ Por favor, llena la descripción y el monto.")

st.divider()

# --- VISUALIZACIÓN DE DATOS ---
conn = sqlite3.connect('negocio_pro.db')
df = pd.read_sql_query("SELECT * FROM transacciones", conn)
conn.close()

if not df.empty:
    # Cálculos de Totales
    ventas = df[df['tipo'] == 'Venta (Ingreso)']['monto'].sum()
    gastos = df[df['tipo'] == 'Gasto (Salida)']['monto'].sum()
    balance = ventas - gastos
    
    # Métricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Ingresos Totales", f"RD$ {ventas:,.2f}")
    m2.metric("Gastos Totales", f"RD$ {gastos:,.2f}", delta=f"-{gastos:,.0f}", delta_color="inverse")
    m3.metric("Ganancia Neta", f"RD$ {balance:,.2f}")

    st.subheader("📋 Historial de Movimientos")
    # Formatear la tabla para que se vea limpia
    df_display = df.drop(columns=['id']).sort_values(by='fecha', ascending=False)
    st.dataframe(df_display, use_container_width=True)

    # Botón para limpiar todo (Cuidado con esto)
    if st.checkbox("Habilitar opción de borrar historial"):
        if st.button("🗑️ Borrar todos los datos", type="primary"):
            conn = sqlite3.connect('negocio_pro.db')
            c = conn.cursor()
            c.execute("DELETE FROM transacciones")
            conn.commit()
            conn.close()
            st.rerun()
else:
    st.info("Aún no hay registros en el sistema. ¡Empieza a digitalizar el negocio!")