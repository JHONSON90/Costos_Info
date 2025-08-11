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

st.placeholder = st.empty()
supabase = init_connection()

def fetch_all_data(query_builder, cursor_column="Mes", page_size=500):
    all_data = []
    last_cursor_value = None
    
    placeholder = st.empty()
    # placeholder.info(f"Cargando datos de la tabla consumos. Un momento por favor...")
    # time.sleep(2)
    # placeholder.empty()

    
    try:
        while True:
            query = query_builder()
            if last_cursor_value is not None:
                query = query.gt(cursor_column, last_cursor_value)

            response = query.order(cursor_column).limit(page_size).execute()
            data_chunk = response.data
            
            if not data_chunk:
                break
            all_data.extend(data_chunk)
            
            placeholder.info(f"Cargando {len(all_data)} registros...")
            time.sleep(1)
            placeholder.empty()

            if len(data_chunk) < page_size:
                break
            else:
                last_cursor_value = data_chunk[-1][cursor_column]
                placeholder.info(f"Cargando {len(all_data)} registros...")
                time.sleep(1)
                placeholder.empty()

    except Exception as e:
        st.error(f"Error al cargar datos de la tabla consumos: {e}")
        st.error(f"Detalles del error: {traceback.format_exc()}")
        return pd.DataFrame()
    return pd.DataFrame(all_data)

@st.cache_data(ttl=3600, show_spinner="Cargando datos de la vista de medicamentos...")
def load_medicamentos_data():
    def query_builder():
        return supabase.table("consumos").select("cc_Nombre, Mes, scc_Nombre, EspeNom, MedicoNom, Producto, NomPaciente,dValor, dCantidad").or_("Linea.eq.MEDICAMENTOS POS, Linea.eq.MEDICAMENTOS NO POS").like("CtaCruce", "6135%")
    return fetch_all_data(query_builder)

@st.cache_data(ttl=3600, show_spinner="Cargando datos de la vista de dispositivos...")
def load_dispositivos_data():
    def query_builder():
        return supabase.table("consumos").select("cc_Nombre, Mes, scc_Nombre, EspeNom, MedicoNom, Producto, NomPaciente, dValor, dCantidad").or_("Linea.neq.MEDICAMENTOS POS, Linea.neq.MEDICAMENTOS NO POS").like("CtaCruce", "6135%").eq("origenMed", "SIMA")
    return fetch_all_data(query_builder)

@st.cache_data(ttl=3600, show_spinner="Cargando datos de la vista de insumos...")
def load_insumos_data():
    def query_builder():
        return supabase.table("consumos").select("cc_Nombre, Mes, scc_Nombre, EspeNom, MedicoNom, Producto, NomPaciente, dValor, dCantidad").or_("Linea.neq.MEDICAMENTOS POS, Linea.neq.MEDICAMENTOS NO POS").like("CtaCruce", "6135%").eq("origenMed", "SIIGO")
    return fetch_all_data(query_builder)


selected_lineas = st.selectbox(
    "Selecciona la linea que quieras revisar: ", 
    ("Medicamentos", "Dispositivos médicos", "Insumos")
)

if selected_lineas == "Medicamentos":
    df = load_medicamentos_data()
    if not df.empty:
        st.success("Datos cargados y procesados exitosamente!")
    else:
        st.info("No se pudieron cargar los datos o la tabla está vacía. Pero no te preocupes te aseguramos que estamos trabajando en solucionar esto!!!")
        st.stop()
elif selected_lineas == "Dispositivos médicos":
    df = load_dispositivos_data()
    if not df.empty:
        st.success("Datos cargados y procesados exitosamente!")
    else:
        st.info("No se pudieron cargar los datos o la tabla está vacía. Pero no te preocupes te aseguramos que estamos trabajando en solucionar esto!!!")
        st.stop()
    st.write("Seleccionaste Dispositivos médicos")
elif selected_lineas == "Insumos":
    df = load_insumos_data()
    if not df.empty:
        st.success("Datos cargados y procesados exitosamente!")
    else:
        st.info("No se pudieron cargar los datos o la tabla está vacía. Pero no te preocupes te aseguramos que estamos trabajando en solucionar esto!!!")
        st.stop()
    st.write("Seleccionaste Insumos")


st.write(df)
df.valor = abs(df.valor)
df.cantidad = abs(df.cantidad)

st.subheader(f"Consumo de {selected_lineas}")
col1, col2 = st.columns([2,1])
with col1:
    pivot_df = df.pivot_table(index="Mes", values="valor", aggfunc="sum").reset_index()
    fig = px.line(pivot_df, x="Mes", y="valor", line_shape="spline")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write(pivot_df)

#     st.subheader("Consumo por Contrato")
    
#     pivot_df = filtered_df.pivot_table(index="cc_Nombre", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#     pivot_df["Total"] = pivot_df.sum(axis=1)
#     pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#     fig = px.bar(filtered_df, x="cc_Nombre", y="dValor", color="NUMERO MES", barmode="group")
#     st.plotly_chart(fig, use_container_width=True)
#     with st.expander("Tabla de consumo por Contrato"):
#         st.write(pivot_df)

#     st.subheader("Consumo por Unidad funcional")
    
#     pivot_df = filtered_df.pivot_table(index="scc_Nombre", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#     pivot_df["Total"] = pivot_df.sum(axis=1)
#     pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#     fig = px.histogram(filtered_df, x="scc_Nombre", y="dValor", color="NUMERO MES", barmode="group")
#     st.plotly_chart(fig, use_container_width=True)
#     with st.expander("Tabla de consumo por Unidad funcional"):
#         st.write(pivot_df)

#     st.multiselect("Para mayor detalle filtra una unidad funcional", filtered_df["scc_Nombre"].unique(), key="unidad_funcional")
#     if st.session_state.unidad_funcional:
#         filtered_df = filtered_df[filtered_df["scc_Nombre"].isin(st.session_state.unidad_funcional)]
#     if not filtered_df.empty:
#         st.subheader("Consumo por especialidad")
#         pivot_df = filtered_df.pivot_table(index="EspeNom", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#         pivot_df["Total"] = pivot_df.sum(axis=1)
#         pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#         fig = px.histogram(filtered_df, y="EspeNom", x="dValor", color="NUMERO MES", barmode="group", height=800)
#         st.plotly_chart(fig, use_container_width=True)
#         with st.expander("Tabla detallada de consumo por especialidad"):
#             st.write(pivot_df)
        
#         st.multiselect("Aqui podemos filtrar por Especialidad", filtered_df["EspeNom"].unique(), key="especialidad")
#         if st.session_state.especialidad:
#             filtered_df = filtered_df[filtered_df["EspeNom"].isin(st.session_state.especialidad)]
#         if not filtered_df.empty:
#             st.subheader("Consumo por medico")
#             pivot_df = filtered_df.pivot_table(index="MedicoNom", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#             pivot_df["Total"] = pivot_df.sum(axis=1)
#             pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#             st.write(pivot_df)

#             st.title("Analisis de consumos por cantidad y valor")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Consumo por medicamento (Analisis por cantidades)")
#                 pivot_df = filtered_df.pivot_table(index="Producto", columns="NUMERO MES", values="dCantidad", aggfunc="sum", fill_value=0)
#                 pivot_df["Total"] = pivot_df.sum(axis=1)
#                 pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#                 with st.expander("Tabla detallada de consumo por medicamento"):
#                     st.write(pivot_df)

#             with col2:
#                 st.subheader("Consumo por medicamento (Analisis por valores)")
#                 pivot_df = filtered_df.pivot_table(index="Producto", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#                 pivot_df["Total"] = pivot_df.sum(axis=1)
#                 pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()
#                 with st.expander("Tabla detallada de consumo por medicamento"):
#                     st.write(pivot_df)

#             st.subheader("Consumo por Paciente")
#             filtered_df = filtered_df[filtered_df["origenMed"] == "SIMA"]
#             pivot_df = filtered_df.pivot_table(index="NomPaciente", columns="NUMERO MES", values="dValor", aggfunc="sum", fill_value=0)
#             pivot_df["Total"] = pivot_df.sum(axis=1)
#             pivot_df = pivot_df.sort_values(by="Total", ascending=False).reset_index()

#             fig = px.box(filtered_df, x="NomPaciente", y="dValor", color="NUMERO MES", height=600)
#             fig.update_traces(quartilemethod="exclusive")
#             st.plotly_chart(fig, use_container_width=True)

#             with st.expander("Tabla detallada de consumo por paciente"):
#                 st.write(pivot_df)

# else:
#     st.write("No hay datos para mostrar con los filtros seleccionados.")
    
    

# #st.write(df)