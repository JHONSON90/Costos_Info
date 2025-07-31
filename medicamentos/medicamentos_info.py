import streamlit as st
import pandas as pd 
import numpy as np
import traceback
import time
import plotly.express as px
import plotly.graph_objects as go
from st_supabase_connection import SupabaseConnection

st.title("Informe de consumos")

@st.cache_resource(show_spinner="Cargando datos. Un momento por favor...")
def init_connection():
       return st.connection("supabase", type=SupabaseConnection)

@st.cache_data( show_spinner="Cargando datos. Un momento por favor...")
def load_data(_conn):
    try:
        rows = _conn.table("consumos").select("*").execute()
        df = pd.DataFrame(rows.data)
        print(df.head(5))
        return df
    
    except Exception as e:
        st.error(f"Error al cargar las variables de entorno: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
        st.stop()

conn = init_connection()
df = load_data(conn)

if not df.empty:
    st.success("Datos cargados y procesados exitosamente!")

else:
    st.info("No se pudieron cargar los datos o la tabla está vacía. Pero no te preocupes te aseguramos que estamos trabajando en solucionar esto!!!")
    st.stop()

df.columns = df.columns.str.strip()

df["fecha"] = pd.to_datetime(df["fecha"], format="%Y%m", errors="coerce")
df["dia"] = df["fecha"].dt.day

df["dCantidad"] = abs(df["dCantidad"])
df["dValor"] = abs(df["dValor"])

df["NUMERO MES"] = df["fecha"].dt.month
df["Ano"] = df["fecha"].dt.year

df["NUMERO MES"] = df["NUMERO MES"].astype(int)
df["Ano"] = df["Ano"].astype(int)
df["dValor"] = df["dValor"].astype(int)
df["dCantidad"] = df["dCantidad"].astype(int)

CODIGO_PREFIJADO = "6135"
df["CtaCruce"] = df["CtaCruce"].astype(str)
df = df[df["CtaCruce"].str.startswith(CODIGO_PREFIJADO, na=False)]

selected_lineas = st.multiselect("Selecciona la linea que quieras revisar", 
                                ["Medicamentos", "Dispositivos médicos", "Insumos"], 
                                key="linea")


filtered_df = df.copy()  

if selected_lineas:  
    conditions = []
    
    for linea in selected_lineas:
        if linea == "Medicamentos":
            conditions.append(df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"]))
        elif linea == "Dispositivos médicos":
            conditions.append((~df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"])) & (df["origenMed"] == "SIMA"))
        elif linea == "Insumos":
            conditions.append((~df["Linea"].isin(["MEDICAMENTOS POS", "MEDICAMENTOS NO POS"])) & (df["origenMed"] == "SIIGO"))
    
    if conditions:
        final_condition = conditions[0]
        for cond in conditions[1:]:
            final_condition |= cond
        filtered_df = df[final_condition]

if not filtered_df.empty:
    st.subheader(f"Consumo de {', '.join(selected_lineas)}" if selected_lineas else "Consumos")
    col1, col2 = st.columns([2,1])
    with col1:
        pivot_df = filtered_df.pivot_table(index="NUMERO MES", values="dValor", aggfunc="sum").reset_index()
        fig = px.line(pivot_df, x="NUMERO MES", y="dValor", line_shape="spline")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write(pivot_df)

    st.subheader("Consumo por Contrato")
    
    pivot_df = filtered_df.pivot_table(index="cc_Nombre", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
    pivot_df["Total"] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
    fig = px.bar(filtered_df, x="cc_Nombre", y="dValor", color="NUMERO MES", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Tabla de consumo por Contrato"):
        st.write(pivot_df)

    st.subheader("Consumo por Unidad funcional")
    
    pivot_df = filtered_df.pivot_table(index="scc_Nombre", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
    pivot_df["Total"] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
    fig = px.histogram(filtered_df, x="scc_Nombre", y="dValor", color="NUMERO MES", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Tabla de consumo por Unidad funcional"):
        st.write(pivot_df)

    st.multiselect("Para mayor detalle filtra una unidad funcional", filtered_df["scc_Nombre"].unique(), key="unidad_funcional")
    if st.session_state.unidad_funcional:
        filtered_df = filtered_df[filtered_df["scc_Nombre"].isin(st.session_state.unidad_funcional)]
    if not filtered_df.empty:
        st.subheader("Consumo por especialidad")
        pivot_df = filtered_df.pivot_table(index="EspeNom", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
        pivot_df["Total"] = pivot_df.sum(axis=1)
        pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
        fig = px.histogram(filtered_df, y="EspeNom", x="dValor", color="NUMERO MES", barmode="group", height=800)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Tabla detallada de consumo por especialidad"):
            st.write(pivot_df)
        
        st.multiselect("Aqui podemos filtrar por Especialidad", filtered_df["EspeNom"].unique(), key="especialidad")
        if st.session_state.especialidad:
            filtered_df = filtered_df[filtered_df["EspeNom"].isin(st.session_state.especialidad)]
        if not filtered_df.empty:
            st.subheader("Consumo por medico")
            pivot_df = filtered_df.pivot_table(index="MedicoNom", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
            pivot_df["Total"] = pivot_df.sum(axis=1)
            pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
            st.write(pivot_df)

            st.title("Analisis de consumos por cantidad y valor")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Consumo por medicamento (Analisis por cantidades)")
                pivot_df = filtered_df.pivot_table(index="Producto", columns="NUMERO MES", values="dCantidad", aggfunc="sum", fill_value=0)
                pivot_df["Total"] = pivot_df.sum(axis=1)
                pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
                with st.expander("Tabla detallada de consumo por medicamento"):
                    st.write(pivot_df)

            with col2:
                st.subheader("Consumo por medicamento (Analisis por valores)")
                pivot_df = filtered_df.pivot_table(index="Producto", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
                pivot_df["Total"] = pivot_df.sum(axis=1)
                pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
                with st.expander("Tabla detallada de consumo por medicamento"):
                    st.write(pivot_df)

            st.subheader("Consumo por Paciente")
            filtered_df = filtered_df[filtered_df["origenMed"] == "SIMA"]
            pivot_df = filtered_df.pivot_table(index="NomPaciente", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
            pivot_df["Total"] = pivot_df.sum(axis=1)
            pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()

            fig = px.box(filtered_df, x="NomPaciente", y="dValor", color="NUMERO MES", height=600)
            fig.update_traces(quartilemethod="exclusive")
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Tabla detallada de consumo por paciente"):
                st.write(pivot_df)

else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")
    
    

#st.write(df)