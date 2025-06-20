import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import plotly.express as px
import plotly.graph_objects as go

st.title("Informe de Costos")

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Informe_costos", ttl=0)
    placeholder = st.empty()
    placeholder.success("Conexión exitosa!")
    time.sleep(2)
    placeholder.empty()
except Exception as e:
    placeholder = st.empty()
    placeholder.error(f"Error al conectar con Google Sheets: {str(e)}")
    placeholder.error(f"Traceback: {traceback.format_exc()}")
    placeholder.empty()


df.columns = df.columns.str.strip()

df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y")
df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce").fillna(0)
df["VALOR"] = df["VALOR"].astype(int)
df["Mes"] = df["FECHA"].dt.month
df["Ano"] = df["FECHA"].dt.year


st.title("Comportamiento mensual de costos")

td_mensual = df.pivot_table(index=["Mes", "Ano"], values="VALOR", aggfunc="sum").reset_index()

fig = px.line(td_mensual, x="Mes", y="VALOR", color="Ano", line_shape="spline")
st.plotly_chart(fig, use_container_width=True)

st.title("Analisis de costos por componente")

td_componentes = df.pivot_table(index="DETALLE", columns="Ano", values="VALOR", aggfunc="sum").reset_index()

fig = px.bar(df, x="DETALLE", y="VALOR", color="Ano", barmode="group")
st.plotly_chart(fig, use_container_width=True)

with st.expander("Tabla detallada de costos por componente"):
    st.write(td_componentes)

st.subheader("Filtros para controlar el dashboard")
col1, col2, col3 = st.columns(3)

with col1:
    st.multiselect("Selecciona un componente", df["DETALLE"].unique(), key="componente")

with col2:
    st.multiselect("Selecciona un año", df["Ano"].unique(), key="anio")

with col3:
    st.multiselect("Selecciona un mes", df["Mes"].unique(), key="mes")


if st.session_state.componente:
    df = df[df["DETALLE"].isin(st.session_state.componente)]
if st.session_state.anio:
    df = df[df["Ano"].isin(st.session_state.anio)]
if st.session_state.mes:
    df = df[df["Mes"].isin(st.session_state.mes)]

if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Costos por componente")
        fig = px.bar(df, x="Mes", y="VALOR", color="Ano", barmode="group", height=600)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Tabla de costos por componentes"):
            st.write(df.pivot_table(index=["Mes", "MES"], columns="Ano", values="VALOR", aggfunc="sum", fill_value=0).reset_index())
    with col2:
        st.subheader("Costos por centro de costo")
        fig = px.bar(df, y="correccion cc", x="VALOR", color="Ano", barmode="group", height=600)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Tabla de costos por centro de costo"):
            st.write(df.pivot_table(index=["Mes", "MES"], columns="Ano", values="VALOR", aggfunc="sum", fill_value=0).reset_index())
