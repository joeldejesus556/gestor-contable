import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Gestor Multi-Cliente Pro", page_icon="🔐", layout="wide")

# 2. --- BASE DE DATOS DE CLIENTES ---
# Aquí es donde gestionas a tus usuarios. ¡Añade más siguiendo el mismo formato!
USUARIOS = {
    "joel_admin": {
        "clave": "1234",
        "id_hoja": "1So7au1zmTk5KQOjh2MKGO41CL4WmYoJMAcCrguj15RI",
        "url_form": "https://forms.gle/tHHCXYrAu7TVqBhE8",
        "nombre_negocio": "Mi Panel de Control"
    },
    "taller_mecanico": {
        "clave": "taller2026",
        "id_hoja": "PON_AQUÍ_EL_ID_DE_LA_COPIA",
        "url_form": "https://forms.gle/tHHCXYrAu7TVqBhE8", # Cambia por el link del nuevo form
        "nombre_negocio": "Taller Los Muchachos"
    }
}

# 3. --- LÓGICA DE AUTENTICACIÓN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso al Sistema de Gestión")
    st.write("Bienvenido. Por favor introduce tus credenciales.")
    
    col1, col2 = st.columns(2)
    with col1:
        user_input = st.text_input("Nombre de Usuario")
    with col2:
        pass_input = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión", use_container_width=True):
        if user_input in USUARIOS and USUARIOS[user_input]["clave"] == pass_input:
            st.session_state.autenticado = True
            st.session_state.usuario_actual = user_input
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos. Intenta de nuevo.")
    st.stop() # Detiene la ejecución aquí si no está logueado

# 4. --- CARGA DE DATOS DEL CLIENTE LOGUEADO ---
cliente = USUARIOS[st.session_state.usuario_actual]
ID_HOJA = cliente["id_hoja"]
URL_FORM = cliente["url_form"]
NOMBRE_NEGOCIO = cliente["nombre_negocio"]

URL_CSV = f"https://docs.google.com/spreadsheets/d/{ID_HOJA}/export?format=csv"

# 5. --- INTERFAZ DEL DASHBOARD ---
st.sidebar.title(f"👤 {st.session_state.usuario_actual}")
st.sidebar.write(f"Negocio: **{NOMBRE_NEGOCIO}**")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

st.title(f"🚀 {NOMBRE_NEGOCIO}")
st.info("Panel de Control Financiero en Tiempo Real")

# Botón de Registro
st.subheader("➕ Registro de Movimientos")
st.link_button(f"📝 Abrir Formulario de {NOMBRE_NEGOCIO}", URL_FORM, use_container_width=True)

st.divider()

# Visualización de Datos
try:
    df = pd.read_csv(URL_CSV)
    
    if not df.empty:
        # Limpieza rápida de la columna Monto
        # (Asegúrate que en tu Excel la columna se llame exactamente 'Monto')
        df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
        
        # Cálculos de Ingresos, Gastos y Neto
        ingresos = df[df['Tipo'].str.contains("Ingreso", na=False)]['Monto'].sum()
        gastos = df[df['Tipo'].str.contains("Gasto", na=False)]['Monto'].sum()
        balance = ingresos - gastos

        # Métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("Ingresos Totales", f"RD$ {ingresos:,.2f}")
        m2.metric("Gastos Totales", f"RD$ {gastos:,.2f}", delta=f"-{gastos:,.2f}", delta_color="inverse")
        m3.metric("Ganancia Neta", f"RD$ {balance:,.2f}")

        st.subheader("📋 Historial de Transacciones")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aún no hay datos registrados para este negocio.")
except Exception as e:
    st.error("⚠️ Error al conectar con la base de datos de Google Sheets.")
    st.write("Verifica que el ID de la hoja sea correcto y esté publicada en la web.")
