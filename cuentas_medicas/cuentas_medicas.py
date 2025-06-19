
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Cuentas_medicas", ttl=0)
    placeholder = st.empty()
    placeholder.success("Conexión exitosa!")
    time.sleep(2)
    placeholder.empty()
except Exception as e:
    placeholder = st.empty()
    placeholder.error(f"Error al conectar con Google Sheets: {str(e)}")
    placeholder.error(f"Traceback: {traceback.format_exc()}")
    placeholder.empty()


st.title("Cuentas Medicas")
st.subheader("Servicios prestados a Proinsalud por parte de otros prestadores")
df.columns = df.columns.str.strip()

df["FECHA"] = pd.to_datetime(df["FECHA"], format="%Y/%m/%d")
df["DEBITOS"] = pd.to_numeric(df["DEBITOS"], errors='coerce').fillna(0).astype(int)
df["CREDITOS"] = pd.to_numeric(df["CREDITOS"], errors='coerce').fillna(0).astype(int)
#df["SALDO"] = df["DEBITOS"] - df["CREDITOS"]
df["SALDO"] = pd.to_numeric(df["SALDO"], errors='coerce').fillna(0).astype(int)
df["Mes"] = df["FECHA"].dt.month
df["Ano"] = df["FECHA"].dt.year

df_2024 = df[df.Ano == 2024]
df_2025 = df[df.Ano == 2025]

td_2024 = df_2024.pivot_table(index="Mes", values="SALDO", aggfunc="sum").reset_index()


promedio_2024 = td_2024['SALDO'].mean()
meses_2024 = len(td_2024['Mes'].unique())
total_2024 = td_2024['SALDO'].sum()

td_2025 = df_2025.pivot_table(index="Mes", values="SALDO", aggfunc="sum").reset_index()

promedio_2025 = td_2025['SALDO'].mean()
meses_2025 = len(td_2025['Mes'].unique())
total_2025 = td_2025['SALDO'].sum()

dif_total = ((total_2025-total_2024)/total_2024)*100
dif_prom = ((promedio_2025-promedio_2024)/promedio_2024)*100

data1, data2, data3,  = st.columns(3, vertical_alignment="center")
data1.metric("Total Cuentas Medicas 2024", f"${total_2024.round(2):,.2f}",  border=True)
data2.metric("Promedio Cuentas Medicas 2024", f"${promedio_2024.round(2):,.2f}", border=True)
data3.metric("Meses de medicion 2024", f"{meses_2024}", border=True)

data4, data5, data6 =st.columns(3, vertical_alignment="center")
data4.metric("Total Cuentas Medicas 2025", f"${total_2025.round(2):,.2f}", f"{dif_total.round(2):,.2f}%", border=True)
data5.metric("Promedio Cuentas Medicas 2025", f"${promedio_2025.round(2):,.2f}", f"{dif_prom.round(2):,.2f}%", border=True)
data6.metric("Meses de medicion 2025", f"{meses_2025}", border=True)

st.subheader("Comportamiento mensual de Cuentas Medicas")

td_mensual = df.pivot_table(index=["Ano", "Mes"], values="SALDO", aggfunc="sum")
td_mensual = td_mensual.reset_index()

fig = px.line(td_mensual, x="Mes", y="SALDO", color="Ano", line_shape="spline")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtros para controlar el dashboard")

unidad_funcional = df["Correccion 2"].unique()

col1, col2, col3 = st.columns(3)

with col1:
    st.multiselect("Selecciona la unidad funcional", unidad_funcional, key="u_funcional")
    
with col2:
    st.multiselect("Selecciona un año", df["Ano"].unique(), key="anio")
    
with col3:
    st.multiselect("Selecciona un mes", df["Mes"].unique(), key="mes")

cuentas_filtrado = df.copy()

if st.session_state.u_funcional:
    cuentas_filtrado = cuentas_filtrado[cuentas_filtrado["Correccion 2"].isin(st.session_state.u_funcional)]
if st.session_state.anio:
    cuentas_filtrado = cuentas_filtrado[cuentas_filtrado["Ano"].isin(st.session_state.anio)]
if st.session_state.mes:
    cuentas_filtrado = cuentas_filtrado[cuentas_filtrado["Mes"].isin(st.session_state.mes)]

if not cuentas_filtrado.empty:
    st.title("Analisis de cuentas medicas por Centro de Costo")
    fig = px.bar(cuentas_filtrado, x="Correccion 1", y="SALDO", color="Ano", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Tabla detalle de Cuentas Medicas por centro de costo"):
        td_centros = cuentas_filtrado.pivot_table(index="Correccion 1", columns=["Ano", "Mes"], values="SALDO", aggfunc="sum", fill_value=0 ).reset_index()
        st.write(td_centros)
    st.title("Analisis detallado por centro de costo")
    st.multiselect("Selecciona el centro de costo para un analisis detallado", cuentas_filtrado["Correccion 1"].unique(), key="list_cc")

    if st.session_state.list_cc:
        cuentas_filtrado = cuentas_filtrado[cuentas_filtrado["Correccion 1"].isin(st.session_state.list_cc)]
    
    if not cuentas_filtrado.empty:

        a, b = st.columns(2)
        with a:
            st.text("Analisis detallado por Proveedor")
            fig = px.bar(cuentas_filtrado, x="SALDO", y="Nombre Proveedor", height=700)
            st.plotly_chart(fig, use_container_width=True)

        with b:
            st.text("Analisis detallado por Cuenta Contable ingresada")
            fig = px.bar(cuentas_filtrado, x="SALDO", y="DESCRIPCION", barmode="group", height=700)
            st.plotly_chart(fig, use_container_width=True)