import streamlit as st
import pandas as pd
import plotly.express as px
import sweetviz as sv
import openpyxl

# ==================================
# CONFIGURACIÓN
# ==================================

st.set_page_config(
    page_title="Análisis de Ventas",
    page_icon="📊",
    layout="wide"
)

# ==================================
# TÍTULO
# ==================================

st.title("📊 Sistema de Análisis de Ventas")

# ==================================
# CARGA DE DATOS
# ==================================

df = pd.read_excel("ventas.xlsx")

st.success("Datos cargados correctamente")

# ==================================
# VISUALIZACIÓN DE DATOS
# ==================================

st.header("📋 Conjunto de Datos")

st.dataframe(df)

# ==================================
# INFORMACIÓN GENERAL
# ==================================

st.header("📈 Información General")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Número de Registros",
        df.shape[0]
    )

with col2:
    st.metric(
        "Número de Variables",
        df.shape[1]
    )

# ==================================
# TIPOS DE DATOS
# ==================================

st.subheader("Tipos de Datos")

st.write(df.dtypes)

# ==================================
# VALORES NULOS
# ==================================

st.subheader("Valores Nulos")

st.write(df.isnull().sum())

# ==================================
# VALORES DUPLICADOS
# ==================================

st.subheader("Valores Duplicados")

st.write(df.duplicated().sum())

# ==================================
# ESTADÍSTICAS DESCRIPTIVAS
# ==================================

st.subheader("Estadísticas Descriptivas")

st.dataframe(df.describe(include="all"))

# ==================================
# PRIMERAS Y ÚLTIMAS FILAS
# ==================================

st.subheader("Primeras Filas")

st.dataframe(df.head())

st.subheader("Últimas Filas")

st.dataframe(df.tail())

# ==================================
# GRÁFICO POR PAÍS
# ==================================

st.header("🌎 Ventas por País")

ventas_pais = (
    df.groupby("pais")["precio"]
    .sum()
    .reset_index()
)

fig_pais = px.bar(
    ventas_pais,
    x="pais",
    y="precio",
    title="Ventas Totales por País"
)

st.plotly_chart(fig_pais)

# ==================================
# GRÁFICO POR CIUDAD
# ==================================

st.header("🏙️ Ventas por Ciudad")

ventas_ciudad = (
    df.groupby("ciudad")["precio"]
    .sum()
    .reset_index()
)

fig_ciudad = px.bar(
    ventas_ciudad,
    x="ciudad",
    y="precio",
    title="Ventas Totales por Ciudad"
)

st.plotly_chart(fig_ciudad)

# ==================================
# FORMAS DE PAGO
# ==================================

st.header("💳 Formas de Pago")

formas_pago = (
    df["forma_pago"]
    .value_counts()
    .reset_index()
)

formas_pago.columns = [
    "Forma de Pago",
    "Cantidad"
]

fig_pago = px.pie(
    formas_pago,
    names="Forma de Pago",
    values="Cantidad",
    title="Distribución de Formas de Pago"
)

st.plotly_chart(fig_pago)

# ==================================
# VENTAS POR AÑO
# ==================================

st.header("📅 Ventas por Año")

ventas_anio = (
    df.groupby("anio")["precio"]
    .sum()
    .reset_index()
)

fig_anio = px.line(
    ventas_anio,
    x="anio",
    y="precio",
    title="Ventas por Año"
)

st.plotly_chart(fig_anio)

# ==================================
# REPORTE SWEETVIZ
# ==================================

st.header("📑 Reporte Automático Sweetviz")

if st.button("Generar Reporte"):

    reporte = sv.analyze(df)

    reporte.show_html(
        "reporte.html",
        open_browser=False
    )

    with open(
        "reporte.html",
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()

    st.components.v1.html(
        html,
        height=1000,
        scrolling=True
    )

    st.success(
        "Reporte generado correctamente"
    )