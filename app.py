import streamlit as st
import pandas as pd
from datetime import date

# Configuración de la página para dispositivos móviles y PC
st.set_page_config(page_title="Gestión de Andamios - Obra", page_icon="🏗️", layout="centered")

# Inicializar Base de Datos en la sesión si no existe
if "df_andamios" not in st.session_state:
    st.session_state.df_andamios = pd.DataFrame([
        {
            "ID Andamio": "AND-001", "N° Permiso": "PT-2026-001", "Sector": "Tanques de Almacenamiento",
            "Fecha Realización": "2026-01-10", "Fecha Desarme": "2026-01-20", 
            "Ancho": 2.0, "Largo": 3.0, "Alto": 6.0, "Volumen": 36.0, 
            "Estado": "Desarmado", "Observaciones": "Trabajo finalizado en norma"
        },
        {
            "ID Andamio": "AND-002", "N° Permiso": "PT-2026-005", "Sector": "Calderas",
            "Fecha Realización": "2026-01-15", "Fecha Desarme": "", 
            "Ancho": 1.5, "Largo": 2.0, "Alto": 8.0, "Volumen": 24.0, 
            "Estado": "Armado / Activo", "Observaciones": "Mantenimiento de tuberías de vapor"
        }
    ])

sectores_list = ["Planta General", "Tanques de Almacenamiento", "Calderas", "Tuberías Exteriores", "Reactor Principal", "Taller de Mantenimiento", "Área de Carga / Descarga", "Subestación Eléctrica"]
estados_list = ["Armado / Activo", "Desarmado", "En Inspección", "Requiere Mantenimiento"]

st.title("🏗️ Control de Andamios")

# Menú de navegación adaptado para celular
menu = st.selectbox("Seleccionar Menú", ["📝 Carga Rápida", "🔍 Consulta y Relevamiento", "📊 Panel de Control", "📋 Base de Datos"])

df = st.session_state.df_andamios

# --- 1. CARGA RÁPIDA ---
if menu == "📝 Carga Rápida":
    st.subheader("Registrar Nuevo Andamio")
    
    with st.form("form_andamio"):
        permiso = st.text_input("N° Permiso de Trabajo *", placeholder="Ej: PT-2026-050")
        sector = st.selectbox("Sector / Equipo", sectores_list)
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_realizacion = st.date_input("Fecha Realización", value=date.today())
        with col2:
            fecha_desarme = st.date_input("Fecha Desarme (Opcional)", value=None)
            
        st.markdown("**Dimensiones (Metros)**")
        c1, c2, c3 = st.columns(3)
        with c1:
            ancho = st.number_input("Ancho", min_value=0.1, value=2.0, step=0.1)
        with c2:
            largo = st.number_input("Largo", min_value=0.1, value=2.0, step=0.1)
        with c3:
            alto = st.number_input("Alto", min_value=0.1, value=4.0, step=0.1)
            
        estado = st.selectbox("Estado Actual", estados_list)
        observaciones = st.text_area("Observaciones / Notas")
        
        submitted = st.form_submit_button("💾 Guardar en el Sistema")
        
        if submitted:
            if not permiso:
                st.error("⚠️ El N° de Permiso es obligatorio.")
            else:
                nuevo_id = f"AND-{len(df) + 1:03d}"
                volumen = ancho * largo * alto
                f_desarme_str = fecha_desarme.strftime("%Y-%m-%d") if fecha_desarme else ""
                
                nuevo_registro = {
                    "ID Andamio": nuevo_id,
                    "N° Permiso": permiso,
                    "Sector": sector,
                    "Fecha Realización": fecha_realizacion.strftime("%Y-%m-%d"),
                    "Fecha Desarme": f_desarme_str,
                    "Ancho": ancho,
                    "Largo": largo,
                    "Alto": alto,
                    "Volumen": volumen,
                    "Estado": estado,
                    "Observaciones": observaciones
                }
                
                st.session_state.df_andamios = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
                st.success(f"¡Éxito! Andamio registrado con ID: **{nuevo_id}**")

# --- 2. CONSULTA Y RELEVAMIENTO ---
elif menu == "🔍 Consulta y Relevamiento":
    st.subheader("Búsqueda en Obra")
    c_busqueda = st.text_input("Ingrese ID o N° de Permiso:", placeholder="Ej: AND-001")
    
    if c_busqueda:
        resultado = df[(df["ID Andamio"].str.contains(c_busqueda, case=False, na=False)) | 
                       (df["N° Permiso"].str.contains(c_busqueda, case=False, na=False))]
        
        if not resultado.empty:
            for _, row in resultado.iterrows():
                st.info(f"📋 **Ficha del Andamio: {row['ID Andamio']}**")
                st.write(f"🔹 **Permiso:** {row['N° Permiso']}")
                st.write(f"🏭 **Sector:** {row['Sector']}")
                st.write(f"📌 **Estado:** {row['Estado']}")
                st.write(f"📐 **Medidas:** {row['Ancho']}m (Ancho) x {row['Largo']}m (Largo) x {row['Alto']}m (Alto)")
                st.write(f"📦 **Volumen Total:** {row['Volumen']} m³")
                st.write(f"📅 **Realización:** {row['Fecha Realización']}")
                if row['Fecha Desarme']:
                    st.write(f"🏁 **Desarme:** {row['Fecha Desarme']}")
                st.write(f"📝 **Observaciones:** {row['Observaciones']}")
                st.markdown("---")
        else:
            st.warning("No se encontró ningún registro con ese dato.")

# --- 3. PANEL DE CONTROL ---
elif menu == "📊 Panel de Control":
    st.subheader("Métricas Generales")
    total = len(df)
    activos = len(df[df["Estado"] == "Armado / Activo"])
    vol_activo = df[df["Estado"] == "Armado / Activo"]["Volumen"].sum()
    
    st.metric("Total Registrados", total)
    st.metric("Andamios Activos", activos)
    st.metric("Volumen Activo Total", f"{vol_activo:,.2f} m³")

# --- 4. BASE DE DATOS ---
elif menu == "📋 Base de Datos":
    st.subheader("Registros Completos")
    st.dataframe(df, use_container_width=True)
