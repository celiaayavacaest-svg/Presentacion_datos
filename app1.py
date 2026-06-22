import streamlit as st
import pandas as pd
import plotly.express as px
import sweetviz as sv
import openpyxl

# ==================================
# CONFIGURACIÓN DE PÁGINA
# ==================================

st.set_page_config(
    page_title="Sistema de Ventas y Limpieza",
    page_icon="📊",
    layout="wide"
)

# ==================================
# ESTILOS PERSONALIZADOS
# ==================================

st.markdown("""
    <style>
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a1a2e;
        }
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] .stRadio > label {
            color: #a0aec0 !important;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-top: 0.75rem;
        }

        /* Banner superior */
        .banner {
            background: linear-gradient(135deg, #16213e 0%, #0f3460 60%, #e94560 100%);
            padding: 2rem 2.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        .banner-icon {
            font-size: 3rem;
            line-height: 1;
        }
        .banner-title {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .banner-sub {
            font-size: 1rem;
            color: #a0aec0;
            margin: 0.25rem 0 0 0;
        }

        /* Métricas */
        [data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem 1.5rem;
        }

        /* Separador sidebar */
        .sidebar-section-label {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #718096;
            padding: 0.5rem 0 0.25rem 0;
        }
    </style>
""", unsafe_allow_html=True)


# ==================================
# CARGAR DATOS
# ==================================

@st.cache_data
def cargar_datos():
    return pd.read_excel("ventas_1.xlsx")

df = cargar_datos()


# ==================================
# SIDEBAR — NAVEGACIÓN
# ==================================

with st.sidebar:

    st.markdown("## 📊 Panel de Control")
    st.markdown("---")

    st.markdown('<p class="sidebar-section-label">📈 Análisis de Ventas</p>', unsafe_allow_html=True)
    seccion_analisis = st.radio(
        "analisis",
        [
            "📋 Conjunto de Datos",
            "📈 Información General",
            "🌎 Ventas por País",
            "🏙️ Ventas por Ciudad",
            "💳 Formas de Pago",
            "📅 Ventas por Año",
            "📑 Reporte Sweetviz",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-section-label">🧹 Limpieza de Datos</p>', unsafe_allow_html=True)
    seccion_limpieza = st.radio(
        "limpieza",
        [
            "🏠 Resumen General",
            "🔍 Valores Nulos",
            "📝 Reemplazar por Valor Fijo",
            "📊 Reemplazar por la Media",
            "🔁 Detectar Duplicados",
            "🗑️ Eliminar Duplicados",
            "🧹 Eliminar Nulos (dropna)",
            "📊 Estadística Descriptiva",
            "🚨 Outliers (Precio)",
            "📏 Dimensiones Dataset",
            "💾 Guardar Dataset Limpio",
            "📋 Dataset Final",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info(f"""
    **Dataset activo**  
    🗂 `ventas_1.xlsx`  
    📌 {df.shape[0]:,} registros · {df.shape[1]} variables  
    ❗ {df.isnull().sum().sum()} nulos  
    🔁 {df.duplicated().sum()} duplicados
    """)


# ==================================
# LÓGICA: detectar sección activa
# Streamlit no resetea radios automáticamente,
# usamos session_state para saber cuál cambió.
# ==================================

if "prev_analisis" not in st.session_state:
    st.session_state.prev_analisis = seccion_analisis
if "prev_limpieza" not in st.session_state:
    st.session_state.prev_limpieza = seccion_limpieza

if seccion_analisis != st.session_state.prev_analisis:
    st.session_state.prev_analisis = seccion_analisis
    st.session_state.modulo = "analisis"
elif seccion_limpieza != st.session_state.prev_limpieza:
    st.session_state.prev_limpieza = seccion_limpieza
    st.session_state.modulo = "limpieza"
elif "modulo" not in st.session_state:
    st.session_state.modulo = "analisis"

modulo = st.session_state.modulo


# ==================================
# BANNER SUPERIOR
# ==================================

if modulo == "analisis":
    banner_icon = "📊"
    banner_title = "Análisis de Ventas"
    banner_sub = seccion_analisis
else:
    banner_icon = "🧹"
    banner_title = "Limpieza de Datos"
    banner_sub = seccion_limpieza

st.markdown(f"""
    <div class="banner">
        <div class="banner-icon">{banner_icon}</div>
        <div>
            <p class="banner-title">{banner_title}</p>
            <p class="banner-sub">{banner_sub}</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==============================================================
# MÓDULO 1: ANÁLISIS DE VENTAS
# ==============================================================

if modulo == "analisis":

    # ── Conjunto de Datos ──────────────────────────────────────
    if seccion_analisis == "📋 Conjunto de Datos":
        st.dataframe(df, use_container_width=True)

    # ── Información General ────────────────────────────────────
    elif seccion_analisis == "📈 Información General":

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Número de Registros", f"{df.shape[0]:,}")
        with col2:
            st.metric("Número de Variables", df.shape[1])

        st.subheader("Tipos de Datos")
        st.write(df.dtypes)

        st.subheader("Valores Nulos")
        st.write(df.isnull().sum())

        st.subheader("Valores Duplicados")
        st.write(df.duplicated().sum())

        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df.describe(include="all"), use_container_width=True)

        st.subheader("Primeras Filas")
        st.dataframe(df.head(), use_container_width=True)

        st.subheader("Últimas Filas")
        st.dataframe(df.tail(), use_container_width=True)

    # ── Ventas por País ────────────────────────────────────────
    elif seccion_analisis == "🌎 Ventas por País":

        ventas_pais = df.groupby("pais")["precio"].sum().reset_index()

        fig = px.bar(
            ventas_pais,
            x="pais",
            y="precio",
            title="Ventas Totales por País",
            color="precio",
            color_continuous_scale="Blues",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Ventas por Ciudad ──────────────────────────────────────
    elif seccion_analisis == "🏙️ Ventas por Ciudad":

        ventas_ciudad = df.groupby("ciudad")["precio"].sum().reset_index()

        fig = px.bar(
            ventas_ciudad,
            x="ciudad",
            y="precio",
            title="Ventas Totales por Ciudad",
            color="precio",
            color_continuous_scale="Teal",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Formas de Pago ─────────────────────────────────────────
    elif seccion_analisis == "💳 Formas de Pago":

        formas_pago = df["forma_pago"].value_counts().reset_index()
        formas_pago.columns = ["Forma de Pago", "Cantidad"]

        fig = px.pie(
            formas_pago,
            names="Forma de Pago",
            values="Cantidad",
            title="Distribución de Formas de Pago",
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Ventas por Año ─────────────────────────────────────────
    elif seccion_analisis == "📅 Ventas por Año":

        ventas_anio = df.groupby("anio")["precio"].sum().reset_index()

        fig = px.line(
            ventas_anio,
            x="anio",
            y="precio",
            title="Ventas por Año",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Reporte Sweetviz ───────────────────────────────────────
    elif seccion_analisis == "📑 Reporte Sweetviz":

        if st.button("⚙️ Generar Reporte"):
            with st.spinner("Generando reporte automático..."):
                reporte = sv.analyze(df)
                reporte.show_html("reporte.html", open_browser=False)

                with open("reporte.html", "r", encoding="utf-8") as f:
                    html = f.read()

            st.components.v1.html(html, height=1000, scrolling=True)
            st.success("✅ Reporte generado correctamente")


# ==============================================================
# MÓDULO 2: LIMPIEZA DE DATOS
# ==============================================================

elif modulo == "limpieza":

    # ── Resumen General ────────────────────────────────────────
    if seccion_limpieza == "🏠 Resumen General":

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros", f"{len(df):,}")
        with c2:
            st.metric("Valores Nulos", df.isnull().sum().sum())
        with c3:
            st.metric("Duplicados", df.duplicated().sum())

    # ── Valores Nulos ──────────────────────────────────────────
    elif seccion_limpieza == "🔍 Valores Nulos":

        nulos = df.isnull().sum().reset_index()
        nulos.columns = ["Columna", "Cantidad"]

        st.dataframe(nulos, use_container_width=True)

        fig = px.bar(nulos, x="Columna", y="Cantidad", title="Valores Nulos por Columna", color="Cantidad", color_continuous_scale="Reds")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Reemplazar por Valor Fijo ──────────────────────────────
    elif seccion_limpieza == "📝 Reemplazar por Valor Fijo":

        df_temp = df.copy()
        for col in df_temp.select_dtypes(include="object").columns:
            df_temp[col] = df_temp[col].fillna("Desconocido")

        st.info("Columnas de texto con nulos reemplazados por **'Desconocido'**")
        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Reemplazar por la Media ────────────────────────────────
    elif seccion_limpieza == "📊 Reemplazar por la Media":

        df_temp = df.copy()
        for col in df_temp.select_dtypes(include=["int64", "float64"]).columns:
            df_temp[col] = df_temp[col].fillna(df_temp[col].mean())

        st.info("Columnas numéricas con nulos reemplazados por la **media de cada columna**")
        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Detectar Duplicados ────────────────────────────────────
    elif seccion_limpieza == "🔁 Detectar Duplicados":

        dup = df[df.duplicated()]
        st.metric("Filas duplicadas encontradas", len(dup))
        if len(dup) > 0:
            st.dataframe(dup.head(20), use_container_width=True)
        else:
            st.success("✅ No se encontraron filas duplicadas")

    # ── Eliminar Duplicados ────────────────────────────────────
    elif seccion_limpieza == "🗑️ Eliminar Duplicados":

        df_temp = df.drop_duplicates()
        eliminados = len(df) - len(df_temp)

        st.metric("Filas eliminadas", eliminados)
        st.metric("Registros restantes", len(df_temp))
        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Eliminar Nulos (dropna) ────────────────────────────────
    elif seccion_limpieza == "🧹 Eliminar Nulos (dropna)":

        df_temp = df.dropna()
        eliminados = len(df) - len(df_temp)

        st.metric("Filas eliminadas", eliminados)
        st.metric("Registros restantes", len(df_temp))
        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Estadística Descriptiva ────────────────────────────────
    elif seccion_limpieza == "📊 Estadística Descriptiva":

        st.dataframe(df.describe(), use_container_width=True)

    # ── Outliers (Precio) ──────────────────────────────────────
    elif seccion_limpieza == "🚨 Outliers (Precio)":

        if "precio" in df.columns:

            col = "precio"
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            li = Q1 - 1.5 * IQR
            ls = Q3 + 1.5 * IQR

            outliers = df[(df[col] < li) | (df[col] > ls)]
            sin_outliers = df[(df[col] >= li) & (df[col] <= ls)]

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Q1", round(Q1, 2))
            with c2:
                st.metric("Q3", round(Q3, 2))
            with c3:
                st.metric("IQR", round(IQR, 2))
            with c4:
                st.metric("Límite inferior", round(li, 2))
            with c5:
                st.metric("Outliers detectados", len(outliers))

            st.subheader("Filas con Outliers")
            st.dataframe(outliers.head(20), use_container_width=True)

            st.subheader("Dataset sin Outliers")
            st.dataframe(sin_outliers.head(20), use_container_width=True)

        else:
            st.error("No existe la columna 'precio' en el dataset")

    # ── Dimensiones ────────────────────────────────────────────
    elif seccion_limpieza == "📏 Dimensiones Dataset":

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Filas", f"{df.shape[0]:,}")
        with c2:
            st.metric("Columnas", df.shape[1])

    # ── Guardar Dataset Limpio ─────────────────────────────────
    elif seccion_limpieza == "💾 Guardar Dataset Limpio":

        df_final = df.copy()

        for col in df_final.select_dtypes(include=["int64", "float64"]).columns:
            df_final[col] = df_final[col].fillna(df_final[col].mean())

        for col in df_final.select_dtypes(include="object").columns:
            df_final[col] = df_final[col].fillna("Desconocido")

        df_final = df_final.drop_duplicates()

        for col in df_final.columns:
            if "fecha" in col.lower():
                df_final[col] = pd.to_datetime(df_final[col], errors="coerce")

        df_final.to_csv("datos_limpios.csv", index=False)

        st.success("✅ Dataset guardado como `datos_limpios.csv`")
        st.metric("Registros guardados", len(df_final))
        st.dataframe(df_final.head(20), use_container_width=True)

    # ── Dataset Final ──────────────────────────────────────────
    elif seccion_limpieza == "📋 Dataset Final":

        df_final = df.copy()

        for col in df_final.select_dtypes(include=["int64", "float64"]).columns:
            df_final[col] = df_final[col].fillna(df_final[col].mean())

        for col in df_final.select_dtypes(include="object").columns:
            df_final[col] = df_final[col].fillna("Desconocido")

        df_final = df_final.drop_duplicates()

        st.metric("Registros finales", len(df_final))
        st.dataframe(df_final.head(50), use_container_width=True)
        st.success("✅ Dataset listo para análisis")