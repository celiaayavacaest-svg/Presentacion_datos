import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import mysql.connector

# ==================================
# CONFIGURACIÓN DE PÁGINA
# ==================================

st.set_page_config(
    page_title="Análisis · Tabla Producto",
    page_icon="📦",
    layout="wide"
)

# ==================================
# ESTILOS PERSONALIZADOS
# ==================================

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0d1117;
        }
        [data-testid="stSidebar"] * {
            color: #c9d1d9 !important;
        }
        [data-testid="stSidebar"] .stRadio > label {
            color: #8b949e !important;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-top: 0.6rem;
        }

        /* Banner superior */
        .banner {
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1f2d3d 100%);
            border: 1px solid #30363d;
            padding: 1.8rem 2.2rem;
            border-radius: 12px;
            margin-bottom: 1.8rem;
            display: flex;
            align-items: center;
            gap: 1.4rem;
        }
        .banner-icon {
            font-size: 2.8rem;
            line-height: 1;
        }
        .banner-badge {
            display: inline-block;
            background: #238636;
            color: #fff;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.15rem 0.6rem;
            border-radius: 20px;
            margin-bottom: 0.35rem;
        }
        .banner-title {
            font-size: 1.7rem;
            font-weight: 800;
            color: #f0f6fc;
            margin: 0;
            letter-spacing: -0.02em;
        }
        .banner-sub {
            font-size: 0.9rem;
            color: #8b949e;
            margin: 0.2rem 0 0 0;
        }

        /* Métricas */
        [data-testid="stMetric"] {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 1rem 1.4rem;
        }
        [data-testid="stMetricLabel"] {
            color: #8b949e !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            color: #f0f6fc !important;
            font-weight: 700 !important;
        }

        /* Label sección sidebar */
        .sidebar-label {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #484f58;
            padding: 0.6rem 0 0.2rem 0;
        }

        /* Tablas */
        [data-testid="stDataFrame"] {
            border: 1px solid #30363d;
            border-radius: 8px;
        }

        /* Info / success boxes */
        .stAlert {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


# ==================================
# CONEXIÓN Y CARGA DE DATOS
# ==================================

@st.cache_data
def cargar_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="isa123",
            database="bd_lavadora"
        )
        df = pd.read_sql("SELECT * FROM producto", conexion)
        conexion.close()
        return df, None
    except Exception as e:
        return None, str(e)

df_original, error_conexion = cargar_datos()

if error_conexion:
    st.error(f"❌ Error de conexión a MySQL: {error_conexion}")
    st.info("Asegúrate de que MySQL esté corriendo y los datos de conexión sean correctos.")
    st.stop()

df = df_original.copy()


# ==================================
# SIDEBAR — NAVEGACIÓN
# ==================================

with st.sidebar:
    st.markdown("## 📦 Tabla Producto")
    st.markdown("---")

    st.markdown('<p class="sidebar-label">🔎 Exploración de Datos</p>', unsafe_allow_html=True)
    seccion_exploracion = st.radio(
        "exploracion",
        [
            "📋 Ver Dataset",
            "📈 Información General",
            "📊 Distribución de Costos",
            "🏷️ Productos por Proveedor",
            "📦 Stock Disponible",
            "🔗 Costo vs Stock",
            "🏆 Top 10 Productos más Caros",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-label">🧹 Limpieza de Datos</p>', unsafe_allow_html=True)
    seccion_limpieza = st.radio(
        "limpieza",
        [
            "🏠 Resumen de Calidad",
            "🔍 Valores Nulos",
            "📝 Rellenar Nulos (Texto → Desconocido)",
            "📊 Rellenar Nulos (Numéricos → Media)",
            "🔁 Detectar Duplicados",
            "🗑️ Eliminar Duplicados",
            "🧹 Eliminar Filas con Nulos",
            "📐 Estadística Descriptiva",
            "🚨 Outliers (Costo)",
            "📏 Dimensiones del Dataset",
            "💾 Guardar Dataset Limpio",
            "✅ Dataset Final Limpio",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Info rápida del dataset
    nulos_total = df.isnull().sum().sum()
    dups_total = df.duplicated().sum()
    st.info(f"""
**Dataset activo**  
🗂 `bd_lavadora · producto`  
📌 {df.shape[0]:,} registros · {df.shape[1]} columnas  
❗ {nulos_total} nulos  
🔁 {dups_total} duplicados
""")


# ==================================
# DETECTAR SECCIÓN ACTIVA
# ==================================

if "prev_exploracion" not in st.session_state:
    st.session_state.prev_exploracion = seccion_exploracion
if "prev_limpieza" not in st.session_state:
    st.session_state.prev_limpieza = seccion_limpieza

if seccion_exploracion != st.session_state.prev_exploracion:
    st.session_state.prev_exploracion = seccion_exploracion
    st.session_state.modulo = "exploracion"
elif seccion_limpieza != st.session_state.prev_limpieza:
    st.session_state.prev_limpieza = seccion_limpieza
    st.session_state.modulo = "limpieza"
elif "modulo" not in st.session_state:
    st.session_state.modulo = "exploracion"

modulo = st.session_state.modulo


# ==================================
# BANNER DINÁMICO
# ==================================

if modulo == "exploracion":
    icono = "🔎"
    titulo = "Exploración de Datos"
    subtitulo = seccion_exploracion
    badge = "ANÁLISIS"
else:
    icono = "🧹"
    titulo = "Limpieza de Datos"
    subtitulo = seccion_limpieza
    badge = "LIMPIEZA"

st.markdown(f"""
    <div class="banner">
        <div class="banner-icon">{icono}</div>
        <div>
            <span class="banner-badge">{badge}</span>
            <p class="banner-title">{titulo}</p>
            <p class="banner-sub">{subtitulo}</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==================================
# HELPER — columnas numéricas y texto
# ==================================

def col_num(dataframe):
    return dataframe.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()

def col_obj(dataframe):
    return dataframe.select_dtypes(include="object").columns.tolist()

# Intentamos detectar columna de costo/precio automáticamente
COSTO_COL = None
for c in df.columns:
    if "costo" in c.lower() or "precio" in c.lower() or "price" in c.lower():
        COSTO_COL = c
        break
if COSTO_COL is None and len(col_num(df)) > 0:
    COSTO_COL = col_num(df)[0]   # fallback a la primera numérica

# Intentamos detectar columna de stock
STOCK_COL = None
for c in df.columns:
    if "stock" in c.lower() or "cantidad" in c.lower() or "quantity" in c.lower():
        STOCK_COL = c
        break

# Columna nombre del producto
NOMBRE_COL = None
for c in df.columns:
    if "nombre" in c.lower() or "name" in c.lower() or "producto" in c.lower():
        NOMBRE_COL = c
        break
if NOMBRE_COL is None:
    NOMBRE_COL = df.columns[0]

# Columna proveedor
PROV_COL = None
for c in df.columns:
    if "proveedor" in c.lower() or "provider" in c.lower() or "supplier" in c.lower() or "id_prov" in c.lower():
        PROV_COL = c
        break


# ==============================================================
# MÓDULO 1 — EXPLORACIÓN DE DATOS
# ==============================================================

if modulo == "exploracion":

    # ── Ver Dataset ──────────────────────────────────────────
    if seccion_exploracion == "📋 Ver Dataset":
        st.subheader("Dataset completo · Tabla `producto`")
        st.dataframe(df, use_container_width=True)

    # ── Información General ──────────────────────────────────
    elif seccion_exploracion == "📈 Información General":

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Filas", f"{df.shape[0]:,}")
        with c2:
            st.metric("Columnas", df.shape[1])
        with c3:
            st.metric("Valores Nulos", df.isnull().sum().sum())
        with c4:
            st.metric("Duplicados", df.duplicated().sum())

        st.markdown("---")

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Tipos de Datos")
            dtype_df = pd.DataFrame({
                "Columna": df.dtypes.index,
                "Tipo": df.dtypes.values.astype(str)
            })
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        with col_b:
            st.subheader("Valores Nulos por Columna")
            nulos_df = df.isnull().sum().reset_index()
            nulos_df.columns = ["Columna", "Nulos"]
            st.dataframe(nulos_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df.describe(include="all"), use_container_width=True)

        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Primeras 5 filas")
            st.dataframe(df.head(), use_container_width=True)
        with col_d:
            st.subheader("Últimas 5 filas")
            st.dataframe(df.tail(), use_container_width=True)

    # ── Distribución de Costos ───────────────────────────────
    elif seccion_exploracion == "📊 Distribución de Costos":

        if COSTO_COL:
            col_izq, col_der = st.columns(2)

            with col_izq:
                fig_hist = px.histogram(
                    df,
                    x=COSTO_COL,
                    nbins=20,
                    title=f"Histograma · {COSTO_COL}",
                    color_discrete_sequence=["#238636"],
                )
                fig_hist.update_layout(
                    plot_bgcolor="#0d1117",
                    paper_bgcolor="#0d1117",
                    font_color="#c9d1d9",
                    bargap=0.05,
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            with col_der:
                fig_box = px.box(
                    df,
                    y=COSTO_COL,
                    title=f"Box Plot · {COSTO_COL}",
                    color_discrete_sequence=["#1f6feb"],
                )
                fig_box.update_layout(
                    plot_bgcolor="#0d1117",
                    paper_bgcolor="#0d1117",
                    font_color="#c9d1d9",
                )
                st.plotly_chart(fig_box, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Mínimo", round(df[COSTO_COL].min(), 2))
            with c2:
                st.metric("Máximo", round(df[COSTO_COL].max(), 2))
            with c3:
                st.metric("Media", round(df[COSTO_COL].mean(), 2))
            with c4:
                st.metric("Mediana", round(df[COSTO_COL].median(), 2))
        else:
            st.warning("No se encontró columna de costo/precio en el dataset.")

    # ── Productos por Proveedor ──────────────────────────────
    elif seccion_exploracion == "🏷️ Productos por Proveedor":

        if PROV_COL:
            prov_counts = df[PROV_COL].value_counts().reset_index()
            prov_counts.columns = [PROV_COL, "Cantidad"]

            fig = px.bar(
                prov_counts,
                x=PROV_COL,
                y="Cantidad",
                title=f"Productos por {PROV_COL}",
                color="Cantidad",
                color_continuous_scale="Teal",
                text="Cantidad",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
                xaxis_title=PROV_COL,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(prov_counts, use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontró columna de proveedor. Columnas disponibles:")
            st.write(list(df.columns))

    # ── Stock Disponible ─────────────────────────────────────
    elif seccion_exploracion == "📦 Stock Disponible":

        if STOCK_COL:
            fig = px.bar(
                df.sort_values(STOCK_COL, ascending=False).head(20),
                x=NOMBRE_COL,
                y=STOCK_COL,
                title=f"Top 20 Productos por {STOCK_COL}",
                color=STOCK_COL,
                color_continuous_scale="Blues",
                text=STOCK_COL,
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
                xaxis_tickangle=-35,
            )
            st.plotly_chart(fig, use_container_width=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Stock Total", f"{int(df[STOCK_COL].sum()):,}")
            with c2:
                st.metric("Stock Promedio", round(df[STOCK_COL].mean(), 1))
            with c3:
                st.metric("Sin Stock (0)", int((df[STOCK_COL] == 0).sum()))
        else:
            st.warning("No se encontró columna de stock/cantidad.")
            st.write("Columnas numéricas disponibles:", col_num(df))

    # ── Costo vs Stock ───────────────────────────────────────
    elif seccion_exploracion == "🔗 Costo vs Stock":

        if COSTO_COL and STOCK_COL:
            fig = px.scatter(
                df,
                x=COSTO_COL,
                y=STOCK_COL,
                hover_name=NOMBRE_COL,
                title=f"Relación entre {COSTO_COL} y {STOCK_COL}",
                color=COSTO_COL,
                color_continuous_scale="Viridis",
                size_max=14,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
            )
            st.plotly_chart(fig, use_container_width=True)

            corr = df[[COSTO_COL, STOCK_COL]].corr().iloc[0, 1]
            st.metric("Correlación de Pearson", round(corr, 4))
        elif COSTO_COL:
            st.warning("No se encontró columna de stock. Se muestra solo el costo.")
            st.dataframe(df[[NOMBRE_COL, COSTO_COL]], use_container_width=True)
        else:
            st.warning("No se encontraron columnas numéricas suficientes.")

    # ── Top 10 más Caros ─────────────────────────────────────
    elif seccion_exploracion == "🏆 Top 10 Productos más Caros":

        if COSTO_COL:
            top10 = df.nlargest(10, COSTO_COL)[[NOMBRE_COL, COSTO_COL]]

            fig = px.bar(
                top10,
                x=NOMBRE_COL,
                y=COSTO_COL,
                title=f"Top 10 Productos por {COSTO_COL}",
                color=COSTO_COL,
                color_continuous_scale="Reds",
                text=COSTO_COL,
            )
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top10.reset_index(drop=True), use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontró columna de costo/precio.")


# ==============================================================
# MÓDULO 2 — LIMPIEZA DE DATOS
# ==============================================================

elif modulo == "limpieza":

    # ── Resumen de Calidad ───────────────────────────────────
    if seccion_limpieza == "🏠 Resumen de Calidad":

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Registros", f"{len(df):,}")
        with c2:
            st.metric("Valores Nulos", df.isnull().sum().sum())
        with c3:
            st.metric("Duplicados", df.duplicated().sum())
        with c4:
            completitud = round((1 - df.isnull().sum().sum() / df.size) * 100, 1)
            st.metric("Completitud", f"{completitud}%")

        st.markdown("---")

        # Mapa de nulos por columna
        nulos_col = df.isnull().sum()
        if nulos_col.sum() > 0:
            fig = px.bar(
                x=nulos_col.index,
                y=nulos_col.values,
                title="Valores Nulos por Columna",
                labels={"x": "Columna", "y": "Cantidad de Nulos"},
                color=nulos_col.values,
                color_continuous_scale="OrRd",
            )
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No hay valores nulos en el dataset.")

    # ── Valores Nulos ────────────────────────────────────────
    elif seccion_limpieza == "🔍 Valores Nulos":

        nulos = df.isnull().sum().reset_index()
        nulos.columns = ["Columna", "Nulos"]
        nulos["% del Total"] = (nulos["Nulos"] / len(df) * 100).round(2)
        nulos["Tipo"] = [str(df[c].dtype) for c in nulos["Columna"]]

        st.dataframe(nulos, use_container_width=True, hide_index=True)

        if nulos["Nulos"].sum() > 0:
            fig = px.bar(
                nulos[nulos["Nulos"] > 0],
                x="Columna",
                y="Nulos",
                title="Columnas con Valores Nulos",
                color="Nulos",
                color_continuous_scale="Reds",
                text="Nulos",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ El dataset no tiene valores nulos.")

    # ── Rellenar Nulos Texto ─────────────────────────────────
    elif seccion_limpieza == "📝 Rellenar Nulos (Texto → Desconocido)":

        df_temp = df.copy()
        columnas_afectadas = []
        for col in col_obj(df_temp):
            if df_temp[col].isnull().sum() > 0:
                df_temp[col] = df_temp[col].fillna("Desconocido")
                columnas_afectadas.append(col)

        if columnas_afectadas:
            st.info(f"Columnas de texto rellenadas con **'Desconocido'**: `{', '.join(columnas_afectadas)}`")
        else:
            st.success("✅ No hay nulos en columnas de texto.")

        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Rellenar Nulos Numéricos ─────────────────────────────
    elif seccion_limpieza == "📊 Rellenar Nulos (Numéricos → Media)":

        df_temp = df.copy()
        columnas_afectadas = []
        for col in col_num(df_temp):
            if df_temp[col].isnull().sum() > 0:
                media = df_temp[col].mean()
                df_temp[col] = df_temp[col].fillna(media)
                columnas_afectadas.append(f"{col} (media={round(media,2)})")

        if columnas_afectadas:
            st.info(f"Columnas numéricas rellenadas con su media: **{', '.join(columnas_afectadas)}**")
        else:
            st.success("✅ No hay nulos en columnas numéricas.")

        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Detectar Duplicados ──────────────────────────────────
    elif seccion_limpieza == "🔁 Detectar Duplicados":

        dup = df[df.duplicated()]
        st.metric("Filas duplicadas encontradas", len(dup))

        if len(dup) > 0:
            st.warning(f"Se encontraron **{len(dup)}** filas duplicadas.")
            st.dataframe(dup.head(20), use_container_width=True)
        else:
            st.success("✅ No se encontraron filas duplicadas en el dataset.")

    # ── Eliminar Duplicados ──────────────────────────────────
    elif seccion_limpieza == "🗑️ Eliminar Duplicados":

        df_temp = df.drop_duplicates()
        eliminados = len(df) - len(df_temp)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros originales", len(df))
        with c2:
            st.metric("Duplicados eliminados", eliminados)
        with c3:
            st.metric("Registros restantes", len(df_temp))

        if eliminados > 0:
            st.warning(f"Se eliminaron {eliminados} filas duplicadas.")
        else:
            st.success("✅ No había duplicados. El dataset queda igual.")

        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Eliminar Filas con Nulos ─────────────────────────────
    elif seccion_limpieza == "🧹 Eliminar Filas con Nulos":

        df_temp = df.dropna()
        eliminados = len(df) - len(df_temp)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros originales", len(df))
        with c2:
            st.metric("Filas eliminadas", eliminados)
        with c3:
            st.metric("Registros restantes", len(df_temp))

        if eliminados > 0:
            st.warning(f"Se eliminaron {eliminados} filas que contenían al menos un valor nulo.")
        else:
            st.success("✅ No había filas con nulos. El dataset queda igual.")

        st.dataframe(df_temp.head(20), use_container_width=True)

    # ── Estadística Descriptiva ──────────────────────────────
    elif seccion_limpieza == "📐 Estadística Descriptiva":

        st.subheader("Variables Numéricas")
        st.dataframe(df.describe(), use_container_width=True)

        if len(col_obj(df)) > 0:
            st.subheader("Variables de Texto")
            st.dataframe(df.describe(include="object"), use_container_width=True)

    # ── Outliers (Costo) ─────────────────────────────────────
    elif seccion_limpieza == "🚨 Outliers (Costo)":

        if COSTO_COL:
            col = COSTO_COL
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

            st.markdown("---")

            fig_box = px.box(
                df,
                y=col,
                title=f"Box Plot · {col} (outliers en rojo)",
                color_discrete_sequence=["#1f6feb"],
            )
            fig_box.update_layout(
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#c9d1d9",
            )
            st.plotly_chart(fig_box, use_container_width=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader(f"Filas con Outliers ({len(outliers)})")
                if len(outliers) > 0:
                    st.dataframe(outliers.head(20), use_container_width=True)
                else:
                    st.success("✅ No se detectaron outliers.")
            with col_b:
                st.subheader(f"Dataset sin Outliers ({len(sin_outliers)} filas)")
                st.dataframe(sin_outliers.head(20), use_container_width=True)
        else:
            st.error("No se encontró columna de costo/precio.")

    # ── Dimensiones ──────────────────────────────────────────
    elif seccion_limpieza == "📏 Dimensiones del Dataset":

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Filas", f"{df.shape[0]:,}")
        with c2:
            st.metric("Columnas", df.shape[1])
        with c3:
            st.metric("Celdas totales", f"{df.size:,}")

        st.markdown("---")
        st.subheader("Estructura de columnas")
        estructura = pd.DataFrame({
            "Columna": df.columns,
            "Tipo de Dato": df.dtypes.values.astype(str),
            "No Nulos": df.count().values,
            "Nulos": df.isnull().sum().values,
            "Únicos": [df[c].nunique() for c in df.columns],
        })
        st.dataframe(estructura, use_container_width=True, hide_index=True)

    # ── Guardar Dataset Limpio ───────────────────────────────
    elif seccion_limpieza == "💾 Guardar Dataset Limpio":

        df_final = df.copy()

        # 1) Rellenar nulos numéricos con media
        for col in col_num(df_final):
            if df_final[col].isnull().sum() > 0:
                df_final[col] = df_final[col].fillna(df_final[col].mean())

        # 2) Rellenar nulos de texto con "Desconocido"
        for col in col_obj(df_final):
            if df_final[col].isnull().sum() > 0:
                df_final[col] = df_final[col].fillna("Desconocido")

        # 3) Eliminar duplicados
        antes = len(df_final)
        df_final = df_final.drop_duplicates()
        dups_elim = antes - len(df_final)

        # 4) Convertir fechas si las hay
        for col in df_final.columns:
            if "fecha" in col.lower() or "date" in col.lower():
                df_final[col] = pd.to_datetime(df_final[col], errors="coerce")

        df_final.to_csv("producto_limpio.csv", index=False)

        st.success("✅ Dataset guardado como `producto_limpio.csv`")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros guardados", len(df_final))
        with c2:
            st.metric("Nulos restantes", df_final.isnull().sum().sum())
        with c3:
            st.metric("Duplicados eliminados", dups_elim)

        st.dataframe(df_final.head(20), use_container_width=True)

    # ── Dataset Final Limpio ─────────────────────────────────
    elif seccion_limpieza == "✅ Dataset Final Limpio":

        df_final = df.copy()

        for col in col_num(df_final):
            df_final[col] = df_final[col].fillna(df_final[col].mean())

        for col in col_obj(df_final):
            df_final[col] = df_final[col].fillna("Desconocido")

        df_final = df_final.drop_duplicates()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Registros finales", len(df_final))
        with c2:
            st.metric("Nulos restantes", df_final.isnull().sum().sum())
        with c3:
            st.metric("Columnas", df_final.shape[1])

        st.dataframe(df_final, use_container_width=True)
        st.success("✅ Dataset listo para análisis y modelado.")