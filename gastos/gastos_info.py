import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import plotly.express as px
import plotly.graph_objects as go

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)


try:
    gastos = conn.read(worksheet="Gastos", ttl=0)
    placeholder = st.empty()
    placeholder.success("Conexión exitosa!")
    time.sleep(2)
    placeholder.empty()
except Exception as e:
    placeholder = st.empty()
    placeholder.error(f"Error al conectar con Google Sheets: {str(e)}")
    placeholder.error(f"Traceback: {traceback.format_exc()}")
    placeholder.empty()


st.title("Gastos")

centros = pd.read_excel("centros_costo.xlsx")
#Index(['Etiquetas de fila', 'TITULO', 'UNIDAD FUNCIONAL'], dtype='object')

gastos.columns = gastos.columns.str.strip()

#Cambiar el nombre de la columna SALDO_MOV. por SALDO_MOV
centros = centros.rename(columns={"Etiquetas de fila": "NOMB SUBC"})
gastos = gastos.rename(columns={"SALDO MOV.": "SALDO"})

#Cambiar formatos y valores
gastos["FECHA"] = pd.to_datetime(gastos["FECHA"], format="%Y/%m/%d")
gastos["SALDO"] = pd.to_numeric(gastos["SALDO"], errors='coerce')
gastos["SALDO"] = gastos["SALDO"].fillna(0)

#sacar meses y años
gastos["MES"] = gastos["FECHA"].dt.month
gastos["ANOS"] = gastos["FECHA"].dt.year
gastos["DIAS"] = gastos["FECHA"].dt.day

combinado = pd.merge(gastos, centros, on="NOMB SUBC", how="left")

centros_costo = combinado["UNIDAD FUNCIONAL"].unique()

data_2024 = combinado[combinado["ANOS"] == 2024]
data_2025 = combinado[combinado["ANOS"] == 2025]

td_2024 = data_2024.pivot_table(index="MES", values="SALDO", aggfunc="sum").reset_index()
promedio_2024 = td_2024['SALDO'].mean()
meses_2024 = len(td_2024['MES'].unique())
total_2024 = td_2024['SALDO'].sum()


td_2025 = data_2025.pivot_table(index="MES", values="SALDO", aggfunc="sum").reset_index()
promedio_2025 = td_2025['SALDO'].mean()
total_2025 = td_2025['SALDO'].sum()
meses_2025 = len(td_2025['MES'].unique())

valor_total_2024 = promedio_2024 * meses_2025
dif_total = (total_2025-total_2024)/total_2025
dif_prom = (promedio_2025-promedio_2024)/promedio_2025

data1, data2, data3,  = st.columns(3, vertical_alignment="center")
data1.metric("Total gastos 2024", f"${total_2024.round(2):,.2f}",  border=True)
data2.metric("Promedio gastos 2024", f"${promedio_2024.round(2):,.2f}", border=True)
data3.metric("Meses de medicion 2024", f"{meses_2024}", border=True)

data4, data5, data6 =st.columns(3, vertical_alignment="center")
data4.metric("Total gastos 2025", f"${total_2025.round(2):,.2f}", f"{dif_total.round(2):,.2f}%", border=True)
data5.metric("Promedio gastos 2025", f"${promedio_2025.round(2):,.2f}", f"{dif_prom.round(2):,.2f}%", border=True)
data6.metric("Meses de medicion 2025", f"{meses_2025}", border=True)


st.subheader("Comportamiento mensual de los gastos")

td_mensual = combinado.pivot_table(index=["ANOS", "MES"], values="SALDO", aggfunc="sum")
td_mensual = td_mensual.reset_index()

fig = px.line(td_mensual, x="MES", y="SALDO", color="ANOS", line_shape="spline")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtros para controlar el dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.multiselect("Selecciona la unidad funcional", centros_costo, key="centro_costo")
    
with col2:
    st.multiselect("Selecciona un año", gastos["ANOS"].unique(), key="anio")
    
with col3:
    st.multiselect("Selecciona un mes", gastos["MES"].unique(), key="mes")
    
combinado_filtrado = combinado.copy()
if st.session_state.centro_costo:
    combinado_filtrado = combinado_filtrado[combinado_filtrado["UNIDAD FUNCIONAL"].isin(st.session_state.centro_costo)]
if st.session_state.anio:
    combinado_filtrado = combinado_filtrado[combinado_filtrado["ANOS"].isin(st.session_state.anio)]
if st.session_state.mes:
    combinado_filtrado = combinado_filtrado[combinado_filtrado["MES"].isin(st.session_state.mes)]

if not combinado_filtrado.empty:
    st.title("Gastos por centro de costo")
    fig = px.bar(combinado_filtrado, x="TITULO", y="SALDO", color="ANOS", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Tabla de gastos por centro de costo"):
        td_centros = combinado_filtrado.pivot_table(index="TITULO", values="SALDO", aggfunc="sum").reset_index() 
        st.write(td_centros)

    st.title("Analisis de gastos por Centro de costo")
    st.text("Si queremos verificar un centro de costo en especifico lo vamos aplicar  el siguiente filtro")
    
    listado_cc = combinado["TITULO"].unique()

    st.multiselect("Selecciona un centro de costo", listado_cc, key="list_cc")
    combinado_filtrado2 = combinado_filtrado.copy()

    if st.session_state.list_cc:
        combinado_filtrado2 = combinado_filtrado[combinado_filtrado["TITULO"].isin(st.session_state.list_cc)]

    if not combinado_filtrado2.empty:
        st.title("Gastos por centro de costo")
        cc_mensual = combinado_filtrado2.pivot_table(index=["ANOS", "MES"], values="SALDO", aggfunc="sum")
        cc_mensual = cc_mensual.reset_index()

        fig = px.line(cc_mensual, x="MES", y="SALDO", color="ANOS", line_shape="spline", title="Comportamiento del gasto por centros de costo")
        st.plotly_chart(fig, use_container_width=True)
        st.text("A continuacion usted podra mirar el detallado por tercero segun filtros aplicados anteriormente")

        with st.expander("Movimiento mensual por tercero"):
            td_xcc = combinado_filtrado2.pivot_table(index=["NIT", "NOMBRE"], columns="MES", values="SALDO", aggfunc="sum", fill_value=0)
            td_xcc["Total"] = td_xcc.sum(axis=1)
            td_xcc = td_xcc.reset_index()
            st.write(td_xcc)

        st.title("Analisis por Cuenta Contable")
        fig = px.bar(combinado_filtrado2, y="CUENTA DESCRIPCION", x="SALDO", color="ANOS", barmode="group", height=800)
        st.plotly_chart(fig, use_container_width=True)
        
    
else:
    st.write("No hay datos para mostrar")
