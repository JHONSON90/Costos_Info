import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import plotly.express as px
import plotly.graph_objects as go

st.title("Informe de Honorarios")

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Honorarios", ttl=0)
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

df["FECHA"] = pd.to_datetime(df["FECHA"], format="%Y/%m/%d")
df["Mes"] = df["FECHA"].dt.month
df["Anio"] = df["FECHA"].dt.year

st.title("Comportamiento mensual de Honorarios")

td_mensual = df.pivot_table(index=["Mes", "Anio"], values="SALDO", aggfunc="sum").reset_index()

fig = px.line(td_mensual, x="Mes", y="SALDO", color="Anio", line_shape="spline")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Honorarios por especialidad")
fig = px.bar(df, x="CORRECCION 1", y="SALDO", color="Anio", barmode="group", height=600)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Filtros para controlar el dashboard")
col1, col2, col3 = st.columns(3)

with col1:
    st.multiselect("Selecciona la especialidad", df["CORRECCION 1"].unique(), key="especialidad")

with col2:
    st.multiselect("Selecciona un año", df["Anio"].unique(), key="anio")

with col3:
    st.multiselect("Selecciona un mes", df["Mes"].unique(), key="mes")

if st.session_state.especialidad:
    df = df[df["CORRECCION 1"].isin(st.session_state.especialidad)]
if st.session_state.anio:
    df = df[df["Anio"].isin(st.session_state.anio)]
if st.session_state.mes:
    df = df[df["Mes"].isin(st.session_state.mes)]
if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Comportamiento mensual por especialidad")
        fig = px.bar(df, x="Mes", y="SALDO", color="Anio", barmode="group", height=600)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Tabla de honorarios por especialidad"):
            st.write(df.pivot_table(index="Mes", columns="Anio", values="SALDO", aggfunc="sum", fill_value=0).reset_index())

    with col2:
        st.subheader("Comportamiento mensual por proveedor")
        fig = px.bar(df, y="PROVEEDOR", x="SALDO", color="Anio", barmode="group", height=600)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Tabla de honorarios por proveedor"):
            st.write(df.pivot_table(index="PROVEEDOR", columns="Anio", values="SALDO", aggfunc="sum", fill_value=0).reset_index())
    st.subheader("Comportamiento mensual por proveedor")

    df = df.pivot_table(index="PROVEEDOR", columns=["Anio", "Mes"], values="SALDO", aggfunc="sum", fill_value=0)
    df["Total"] = df.sum(axis=1)
    df = df.sort_values(by="Total", ascending=False).reset_index()
    st.write(df)