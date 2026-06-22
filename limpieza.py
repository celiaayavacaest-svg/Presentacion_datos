import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Sistema de Limpieza de Datos",
    page_icon="🧹",
    layout="wide"
)

# ==========================================
# CARGAR DATOS
# ==========================================
df = pd.read_excel("ventas_1.xlsx")

# ==========================================
# SIDEBAR / MENÚ
# ==========================================
with st.sidebar:

    st.title("🧹 Dashboard")

    st.markdown("---")

    pagina = st.radio(
        "📌 Navegación",
        [
            "🏠 Inicio",
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
            "📋 Dataset Final"
            
        ]
    )

    st.markdown("---")

    st.info("""
    ### Proyecto de Limpieza de Datos

    ✔ Valores nulos  
    ✔ Duplicados  
    ✔ Outliers (precio)  
    ✔ Estadística descriptiva  
    ✔ Dataset final limpio  
    """)

# ==========================================
# INICIO
# ==========================================
if pagina == "🏠 Inicio":

    st.title("🧹 Sistema de Limpieza y Análisis de Datos")

    st.success("Dataset cargado correctamente")

    st.metric("Registros", len(df))
    st.metric("Nulos", df.isnull().sum().sum())
    st.metric("Duplicados", df.duplicated().sum())

# ==========================================
# VALORES NULOS
# ==========================================
elif pagina == "🔍 Valores Nulos":

    st.title("Valores Nulos")

    nulos = df.isnull().sum().reset_index()
    nulos.columns = ["Columna", "Cantidad"]

    st.dataframe(nulos, use_container_width=True)

    st.plotly_chart(
        px.bar(nulos, x="Columna", y="Cantidad"),
        use_container_width=True
    )

# ==========================================
# REEMPLAZAR POR VALOR FIJO
# ==========================================
elif pagina == "📝 Reemplazar por Valor Fijo":

    st.title("Reemplazo por Valor Fijo")

    df_temp = df.copy()

    for col in df_temp.select_dtypes(include="object").columns:
        df_temp[col] = df_temp[col].fillna("Desconocido")

    st.dataframe(df_temp.head(20))

# ==========================================
# REEMPLAZAR POR MEDIA
# ==========================================
elif pagina == "📊 Reemplazar por la Media":

    st.title("Reemplazo por la Media")

    df_temp = df.copy()

    for col in df_temp.select_dtypes(include=["int64", "float64"]).columns:
        df_temp[col] = df_temp[col].fillna(df_temp[col].mean())

    st.dataframe(df_temp.head(20))

# ==========================================
# DUPLICADOS
# ==========================================
elif pagina == "🔁 Detectar Duplicados":

    st.title("Duplicados")

    dup = df[df.duplicated()]

    st.metric("Duplicados", len(dup))
    st.dataframe(dup.head(20))

elif pagina == "🗑️ Eliminar Duplicados":

    st.title("Eliminar Duplicados")

    df_temp = df.drop_duplicates()

    st.metric("Eliminados", len(df) - len(df_temp))
    st.dataframe(df_temp.head(20))

# ==========================================
# NULOS
# ==========================================
elif pagina == "🧹 Eliminar Nulos (dropna)":

    st.title("Eliminar Nulos")

    df_temp = df.dropna()

    st.metric("Eliminados", len(df) - len(df_temp))
    st.dataframe(df_temp.head(20))

# ==========================================
# 📊 ESTADÍSTICA DESCRIPTIVA
# ==========================================
elif pagina == "📊 Estadística Descriptiva":

    st.title("Estadística Descriptiva")

    st.dataframe(df.describe(), use_container_width=True)

# ==========================================
# 🚨 OUTLIERS SOLO PRECIO
# ==========================================
elif pagina == "🚨 Outliers (Precio)":

    st.title("Outliers en Precio (IQR)")

    if "precio" in df.columns:

        col = "precio"

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        li = Q1 - 1.5 * IQR
        ls = Q3 + 1.5 * IQR

        outliers = df[(df[col] < li) | (df[col] > ls)]
        sin_outliers = df[(df[col] >= li) & (df[col] <= ls)]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Q1", round(Q1, 2))
        with c2:
            st.metric("Q3", round(Q3, 2))
        with c3:
            st.metric("Outliers", len(outliers))

        st.subheader("Outliers")
        st.dataframe(outliers.head(20))

        st.subheader("Sin Outliers")
        st.dataframe(sin_outliers.head(20))

    else:
        st.error("No existe la columna 'precio'")

# ==========================================
# 📏 DIMENSIONES
# ==========================================
elif pagina == "📏 Dimensiones Dataset":

    st.title("Dimensiones del Dataset")

    st.metric("Filas", df.shape[0])
    st.metric("Columnas", df.shape[1])

# ==========================================
# 💾 GUARDAR DATASET LIMPIO
# ==========================================
elif pagina == "💾 Guardar Dataset Limpio":

    st.title("Guardar Dataset")

    df_final = df.copy()

    # nulos
    for col in df_final.select_dtypes(include=["int64", "float64"]).columns:
        df_final[col] = df_final[col].fillna(df_final[col].mean())

    for col in df_final.select_dtypes(include="object").columns:
        df_final[col] = df_final[col].fillna("Desconocido")

    # duplicados
    df_final = df_final.drop_duplicates()

    # fechas (si existen)
    for col in df_final.columns:
        if "fecha" in col.lower():
            df_final[col] = pd.to_datetime(df_final[col], errors="coerce")

    df_final.to_csv("datos_limpios.csv", index=False)

    st.success("Dataset guardado como datos_limpios.csv")
    st.dataframe(df_final.head(20))

# ==========================================
# 📋 DATASET FINAL
# ==========================================
elif pagina == "📋 Dataset Final":

    st.title("Dataset Final Limpio")

    df_final = df.copy()

    for col in df_final.select_dtypes(include=["int64", "float64"]).columns:
        df_final[col] = df_final[col].fillna(df_final[col].mean())

    for col in df_final.select_dtypes(include="object").columns:
        df_final[col] = df_final[col].fillna("Desconocido")

    df_final = df_final.drop_duplicates()

    st.metric("Registros finales", len(df_final))
    st.dataframe(df_final.head(50))

    st.success("Dataset listo para análisis")