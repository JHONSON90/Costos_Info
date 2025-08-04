import streamlit as st
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import calendar
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)


try:
    df = conn.read(worksheet="Nomina", ttl=0)
    cargos = conn.read(worksheet="Cargos", ttl=0)
    placeholder = st.empty()
    placeholder.success("Conexión exitosa!")
    time.sleep(2)
    placeholder.empty()
except Exception as e:
    placeholder = st.empty()
    placeholder.error(f"Error al conectar con Google Sheets: {str(e)}")
    placeholder.error(f"Traceback: {traceback.format_exc()}")
    placeholder.empty()

datos = {"C. DE COSTOS": ['101       ALMACEN','102       AUDITORIA INTER','103       CARTERA','104       CONSTRUCCIÓN','105       CONTABILIDAD','106       CONTRATACION','107       COMPRAS','108       COSTOS','109       ESTADISTICA','110       FACTURACION','111       GERENCIA GENERA','112       GERENCIAMIENTO','113       GESTION AMBIENT','114       GESTION DOCUMEN','115       HISTORIAS CLINI','116       JURIDICA','117       PAGADURIA','118       INVESTIG DESAR','119       RECURSOS HUMANO','120       SSST (INTERNO)','121       TECNOLOGIA DE I','122       SUBGERENCIA ADT','123       MANTENIMIENTO','124       ORIENTACIÓN Y V','125       SERVICIOS GENER','129       ADMISIONES','201       ATENCION AL USU','202       COORDINACION MU','207       AUDITORIA MEDIC','301       MEDICINA GENERA','302       PROMOCION Y PRE','303       CRONICOS','307       ODONTOLOGIA','308       SALUD OCUPACION','311       CITAS MEDICAS','312       EPIDEMIOLOGIA','313       PROGRAMA IAMI -','314       SALUD MENTAL','315       SEGURIDAD DEL P','316       SERVICIO FARMAC','321       TERAPIA ONCOLOG','323       ECIS PyM','324       HUMANIZACION','401       HOSPITALIZACION','402       QUIROFANO','403       UCIA','404       UCIN','407       LAVANDERIA','408       URGENCIAS','AMBULANCIA','CAMILLERO','501       LABORATORIO','502       IMAGENOLOGIA','305       MEDICINA ESPECI','101 ALMACEN','102 AUDITORIA INTER','103 CARTERA','104 CONSTRUCCIÓN','105 CONTABILIDAD','106 CONTRATACION','107 COMPRAS','108 COSTOS','109 ESTADISTICA','110 FACTURACION','111 GERENCIA GENERA','112 GERENCIAMIENTO','113 GESTION AMBIENT','114 GESTION DOCUMEN','115 HISTORIAS CLINI','116 JURIDICA','117 PAGADURIA','118 INVESTIG DESAR','119 RECURSOS HUMANO','120 SSST (INTERNO)','121 TECNOLOGIA DE I','122 SUBGERENCIA ADT','123 MANTENIMIENTO','124 ORIENTACIÓN Y V','125 SERVICIOS GENER','126 SUBGERENCIA DE','129 ADMISIONES','201 ATENCION AL USU','202 COORDINACION MU','207 AUDITORIA MEDIC','301 MEDICINA GENERA','302 PROMOCION Y PRE','303 CRONICOS','307 ODONTOLOGIA','308 SALUD OCUPACION','311 CITAS MEDICAS','312 EPIDEMIOLOGIA','314 SALUD MENTAL','315 SEGURIDAD DEL P','316 SERVICIO FARMAC','321 TERAPIA ONCOLOG','323 ECIS PyM','401 HOSPITALIZACION','402 QUIROFANO','403 UCIA','404 UCIN','407 LAVANDERIA','408 URGENCIAS','501 LABORATORIO','502 IMAGENOLOGIA','305 MEDICINA ESPECI'], 
"CLASIFICACION": ['Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Consulta Externa','Consulta Externa','Consulta Externa','Consulta Externa','Consulta Externa','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Consulta Externa','Apoyo Asistencial','Apoyo Asistencial','Apoyo Terapeutico','Consulta Externa','Apoyo Asistencial','Hospitalizacion','Quirofano','Hospitalizacion','Hospitalizacion','Apoyo Asistencial','Urgencias','Apoyo Asistencial','Apoyo Asistencial','Apoyo Diagnostico','Apoyo Diagnostico','Consulta Externa','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Administrativo','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Apoyo Asistencial','Consulta Externa','Consulta Externa','Consulta Externa','Consulta Externa','Consulta Externa','Apoyo Asistencial','Apoyo Asistencial','Consulta Externa','Apoyo Asistencial','Apoyo Asistencial','Apoyo Terapeutico','Consulta Externa','Hospitalizacion','Quirofano','Hospitalizacion','Hospitalizacion','Apoyo Asistencial','Urgencias','Apoyo Diagnostico','Apoyo Diagnostico','Consulta Externa'],
"C_correccion": ['Almacen','Auditoria Interna','Cartera','Construccion','Contabilidad','Contratacion','Compras','Costos','Estadistica','Facturacion','Gerencia General','Gerenciamiento del SGC','Gestion Ambiental','Gestion Documental','Historias Clinicas','Juridica','Pagaduria','Investigacion, desarrollo e Innovacion','Recursos Humanos','SSST Interno','Tecnologia de la Informacion','Subgerencia Administrativa','Mantenimiento','Orientacion y Vigilancia','Servicios Generales','Admisiones','Atencion al Usuario','Coordinacion de Municipios','Auditoria Medica','Medicina General','Promocion y Mantenimiento','Cronicos','Odontologia','Salud Ocupacional','Citas Medicas','Epidemiologia','Programa IAMI','Salud Mental','Seguridad del Paciente','Servicio Farmaceutico','Terapias Oncologicas','ECIS','Humanizacion','Hospitalizacion','Quirofano','Uci Adultos','Uci Neonatal','Lavanderia','Urgencias','Ambulancia','Camilleros','Laboratorio Clinico','Imagenologia','Medicina Especializada','Almacen','Auditoria Interna','Cartera','Construccion','Contabilidad','Contratacion','Compras','Costos','Estadistica','Facturacion','Gerencia General','Gerenciamiento del SGC','Gestion Ambiental','Gestion Documental','Historias Clinicas','Juridica','Pagaduria','Investigacion, desarrollo e Innovacion','Recursos Humanos','SSST Interno','Tecnologia de la Informacion','Subgerencia Administrativa','Mantenimiento','Orientacion y Vigilancia','Servicios Generales','Subgencia de Salud','Admisiones','Atencion al Usuario','Coordinacion de Municipios','Auditoria Medica','Medicina General','Promocion y Mantenimiento','Cronicos','Odontologia','Salud Ocupacional','Citas Medicas','Epidemiologia','Salud Mental','Seguridad del Paciente','Servicio Farmaceutico','Terapias Oncologicas','ECIS','Hospitalizacion','Quirofano','Uci Adultos','Uci Neonatal','Lavanderia','Urgencias','Laboratorio Clinico','Imagenologia','Medicina Especializada']
}
nuevos_cc = pd.DataFrame(datos)

df = df.merge(nuevos_cc, on="C. DE COSTOS", how="left" )
df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y")
df["mes"] = df['FECHA'].dt.month_name()
df["Mes"] = df["FECHA"].dt.month
#df = df.loc[df.mes.isin(["January", "February", "March"])]

st.title("Nomina")

st.title("Comportamiento de Nomina mensual")

promedio_trabajadores = df['GRAN TOTAL'].count() / len(df['Mes'].unique())
promedio_mensual = df['GRAN TOTAL'].sum() / len(df['Mes'].unique())

data1, data2, data3, data4 = st.columns(4, vertical_alignment="center")
data1.metric("Promedio Costo por trabajador",f"${df['GRAN TOTAL'].mean().round(2):,.2f}", border=True)
data2.metric("Promedio Trabajadores Mes", f"{promedio_trabajadores.round(0):,.0f}", border=True)
data3.metric("Total Nomina", f"${df['GRAN TOTAL'].sum().round(2):,.2f}", border=True)
data4.metric("Promedio Mensual",f"${promedio_mensual.round(2):,.2f}", border=True)

st.empty()

col1, col2 = st.columns(2, vertical_alignment="top")
with col1:    
    total_mes = df.groupby("mes")["C_correccion"].count().astype(int)

    fig = px.pie(total_mes, names=total_mes.index, values=total_mes.values)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    total_por_mes = df.groupby("mes").agg(
        num_empleados = ('C_correccion', 'count'),
        total_gt = ('GRAN TOTAL', 'sum'),
    )
    st.write(total_por_mes)


st.title("Analisis por Administrativos y Asistenciales")

fig = px.pie(df, names="CLASIFICACION", title="Porcentaje de Nomina por Administrativos y Asistenciales")
st.plotly_chart(fig, use_container_width=True)

administrativos = df[df["CLASIFICACION"] == "Administrativo"]
asistenciales = df[df["CLASIFICACION"] != "Administrativo"]

admon, asis = st.columns(2, vertical_alignment="center")

with admon:
    fig = px.bar(administrativos, y="C_correccion", x="GRAN TOTAL", color="GRAN TOTAL", title="Nomina por Administrativos", height=600)
    st.plotly_chart(fig, use_container_width=True)
    td_admon = administrativos.pivot_table(index="C_correccion", columns="mes", values="GRAN TOTAL", aggfunc="sum")
    td_admon["Total"] = td_admon.sum(axis=1)
    with st.expander("Tabla de Nomina por Administrativos"):
        st.write(td_admon)

with asis:
    fig2 = px.bar(asistenciales, y="C_correccion", x="GRAN TOTAL", color="GRAN TOTAL", title="Nomina por Asistenciales", height=600)
    st.plotly_chart(fig2, use_container_width=True)
    td_asis = asistenciales.pivot_table(index="C_correccion", columns="mes", values="GRAN TOTAL", aggfunc="sum")
    td_asis["Total"] = td_asis.sum(axis=1)
    with st.expander("Tabla de Nomina por Asistenciales"):
        st.write(td_asis)


st.title("Analisis de Nomina por C. de Costos")

tabla_x_cc = df.pivot_table(index="C_correccion", columns="mes", values="GRAN TOTAL", aggfunc="sum")
tabla_X_cc_und = df.pivot_table(index="C_correccion", columns="mes", values="GRAN TOTAL", aggfunc="count")

grafica_x_cc = df.groupby(["C_correccion", "mes"]).agg(
    num_empleados = ('C_correccion', 'count'),
    total_gt = ('GRAN TOTAL', 'sum'),
).sort_values(by="total_gt", ascending=False).reset_index()

fig = px.scatter(grafica_x_cc,
x="num_empleados", 
y="total_gt", 
size="total_gt", 
color="mes", 
hover_name="C_correccion", 
size_max=60, 
color_discrete_sequence=px.colors.qualitative.Set1
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Tabla de Nomina por C. de Costos"):
    st.write(tabla_x_cc)

with st.expander("Tabla de Nomina por C. de Costos y numero de trabajadores"):
    st.write(tabla_X_cc_und)

st.title("Analisis por cargos")

df2 = df.copy()

df_cargos = df2.merge(cargos, on="CARGO", how="left")

secc1, secc2 = st.columns(2, vertical_alignment="center")
with secc1:
    st.text("Tabla de Nomina por Cargos")
    
    td_cargos = df_cargos.pivot_table(index="CORRECCION", columns="mes", values="GRAN TOTAL", aggfunc="sum")
    td_cargos["Total"] = td_cargos.sum(axis=1)
    
    cargos_nulos = df_cargos.CORRECCION.isnull().sum()
    if cargos_nulos > 0:
        st.warning(f"Se encontraron {cargos_nulos} filas con valores nulos en la columna de ' Cargos'.")
    st.write(td_cargos)
with secc2:
    st.text("Grafica de Nomina por Cargos")
    #td_cargos = td_cargos.loc[:, td_cargos.columns != "Total"]
    fig = px.bar(td_cargos, x=td_cargos.index, y=[col for col in td_cargos.columns if col != "Total"])

    st.plotly_chart(fig, use_container_width=True)
   
def obtener_mes_anterior(mes_actual_str):
    meses_a_numero = {name: num for num, name in enumerate(calendar.month_name) if num}
    numero_a_meses = {num: name for num, name in enumerate(calendar.month_name) if num}

    mes_actual_lower = mes_actual_str.lower()
    if mes_actual_lower.capitalize() not in meses_a_numero:
        st.error(f"Error: '{mes_actual_str}' no es un nombre de mes válido.")
        return None

    numero_mes_actual = meses_a_numero[mes_actual_lower.capitalize()]

    if numero_mes_actual == 1:
        numero_mes_anterior = 12
    else:
        numero_mes_anterior = numero_mes_actual - 1

    return numero_a_meses[numero_mes_anterior]

def mostrar_cambios_empleados(df, mes_actual_str, mes_anterior_str, col4, col5):   
    df_mes_actual = df[df["mes"] == mes_actual_str]
    df_mes_anterior = df[df["mes"] == mes_anterior_str]

    # Calcular nuevos empleados
    cedulas_mes_actual = set(df_mes_actual["CEDULA"])
    cedulas_mes_anterior = set(df_mes_anterior["CEDULA"])

    nuevos_empleados_cedulas = list(cedulas_mes_actual - cedulas_mes_anterior)
    
    # Filtrar el DataFrame para obtener los datos de los nuevos empleados
    nuevos_empleados_df = df_mes_actual[df_mes_actual["CEDULA"].isin(nuevos_empleados_cedulas)]

    if not nuevos_empleados_df.empty:
        imprimir_x_cc_nuevos = nuevos_empleados_df.groupby("C. DE COSTOS").agg(
            num_empleados=('C. DE COSTOS', 'count'),
            total_gt=('GRAN TOTAL', 'sum'),
        ).sort_values(by="total_gt", ascending=False).reset_index()

        with col5:
            st.subheader(f"Resumen de Nuevos Empleados en {mes_actual_str} por C. de Costos")
            st.write(imprimir_x_cc_nuevos)
        
        with col4:
            # Usar una clave única para el multiselect si se usa dentro de una función
            centros_costo_nuevos = st.multiselect(
                f"Selecciona la unidad funcional para filtrar los nuevos empleados de {mes_actual_str}",
                nuevos_empleados_df["C. DE COSTOS"].unique(),
                key=f"centro_costo_nuevos_{mes_actual_str}"
            )

        df_nuevos_filtrado = nuevos_empleados_df.copy()
        if centros_costo_nuevos:
            df_nuevos_filtrado = df_nuevos_filtrado[df_nuevos_filtrado["C. DE COSTOS"].isin(centros_costo_nuevos)]

        imprimir_nuevos = df_nuevos_filtrado.groupby(["CEDULA", "NOMBRE EMPLEADO", "CARGO"])["GRAN TOTAL"].sum().reset_index()
        
        with st.expander(f"Para mirar los nuevos empleados de {mes_actual_str} clickea aquí"):
            st.write(imprimir_nuevos)
    else:
        with col5:
            st.info(f"No hay nuevos empleados en {mes_actual_str} comparado con {mes_anterior_str}.")


    # Calcular empleados salientes
    empleados_salientes_cedulas = list(cedulas_mes_anterior - cedulas_mes_actual)
    
    # Filtrar el DataFrame para obtener los datos de los empleados salientes
    empleados_salientes_df = df_mes_anterior[df_mes_anterior["CEDULA"].isin(empleados_salientes_cedulas)]

    if not empleados_salientes_df.empty:
        imprimir_salida = empleados_salientes_df.groupby(["CEDULA", "NOMBRE EMPLEADO", "CARGO"])['GRAN TOTAL'].sum().reset_index()

        with st.expander(f"Para mirar los empleados que salieron en {mes_actual_str} (comparado con {mes_anterior_str}) clickea aquí"):
            st.write(imprimir_salida)
    else:
        with st.expander(f"Para mirar los empleados que salieron en {mes_actual_str} (comparado con {mes_anterior_str}) clickea aquí"):
            st.info(f"No hay empleados que salieron en {mes_actual_str} comparado con {mes_anterior_str}.")


st.title("Análisis de Movimientos de Empleados por Mes")

col4, col5 = st.columns(2, vertical_alignment="center")

with col4:
    meses_disponibles = df["mes"].unique()
    radio_mes = st.radio("Selecciona un mes", meses_disponibles, index=0)


if radio_mes == "January":
    enero = df[df["mes"] == "January"]
    febrero = df[df["mes"] == "February"]

    salida_enero_feb = np.setdiff1d(enero["CEDULA"], febrero["CEDULA"])
    salida_ener_febrero = df.loc[(df.mes == "January") & (df["CEDULA"].isin(salida_enero_feb))]
    imprimir_salida_enero = salida_ener_febrero.groupby(["CEDULA", "NOMBRE EMPLEADO"])["GRAN TOTAL"].sum().reset_index()
    salidasxcc = salida_ener_febrero.groupby('C. DE COSTOS').agg(
        num_empleados = ('C. DE COSTOS', 'count'),
        total_gt = ('GRAN TOTAL', 'sum'),
        ).sort_values(by="total_gt", ascending=False).reset_index()
    
    with col5:
        st.write(salidasxcc)

    st.write("No se tienen datos para comparación de nuevos ingresos")

    with st.expander("Para mirar los empleados que salieron clickea aqui"):
         st.write(imprimir_salida_enero)

else:
    mes_anterior = obtener_mes_anterior(radio_mes)
    if mes_anterior: # Asegurarse de que se haya encontrado un mes anterior válido
        st.write(f"Comparando {radio_mes} con {mes_anterior}")
        mostrar_cambios_empleados(df, radio_mes, mes_anterior, col4, col5)

st.title("Analisis de Nomina por ingresos del trabajador")

df3 = df.copy()
df3["FECHA"] = pd.to_datetime(df3["FECHA"], format="%d/%m/%Y")
df3 = df3.set_index('FECHA')
ingresos = df3.resample("M")[["BASICO", "VACACIONES DISFRU", "HORAS ADICIONALES", "APOYO DE SOSTENIMIENTO", "OTROS DEVENGOS", "REINTEGROS", "INCAP. ENFERMEDAD"]].sum()


fig = make_subplots(rows=2, cols=4, subplot_titles=["BASICO", "VACACIONES DISFRU", "HORAS ADICIONALES", "APOYO DE SOSTENIMIENTO", "OTROS DEVENGOS", "REINTEGROS", "INCAP. ENFERMEDAD"])

for i, ingreso in enumerate(ingresos):
    row = i // 4 + 1
    col = i % 4 + 1
    fig.add_trace(go.Scatter(x=ingresos.index, y=ingresos[ingreso], mode="lines", name=ingreso), row=row, col=col)

st.plotly_chart(fig, use_container_width=True)

st.title("Analisis de Nomina por Aportes y Parafiscales")

df4 = df.copy()
df4["FECHA"] = pd.to_datetime(df4["FECHA"], format="%d/%m/%Y")
df4 = df4.set_index('FECHA')
aportes = df4.resample("M")[["SENA", "ICBF", "CAJA", "SALUD", "PENSION", "ARL"]].sum()

fig2 = make_subplots(rows=2, cols=3, subplot_titles=["SENA", "ICBF", "CAJA", "SALUD", "PENSION", "ARL"])
for i, aporte in enumerate(aportes):
    row = i // 3 + 1
    col = i % 3 + 1
    fig2.add_trace(go.Scatter(x=aportes.index, y=aportes[aporte], mode="lines", name=aporte), row=row, col=col)

st.plotly_chart(fig2, use_container_width=True)

st.title("Analisis de Nomina por Provisiones")

df5 = df.copy()
df5["FECHA"] = pd.to_datetime(df5["FECHA"], format="%d/%m/%Y")
df5 = df5.set_index('FECHA')
provisiones = df5.resample("M")[["CESANTIAS", "INT. CESANTIAS", "PRIMA DE SERVICIOS", "VACACIONES"]].sum()


fig3 = make_subplots(rows=1, cols=4, subplot_titles=["CESANTIAS", "INT. CESANTIAS", "PRIMA DE SERVICIOS", "VACACIONES"])
for i, provision in enumerate(provisiones):
    row = i // 4 + 1
    col = i % 4 + 1
    fig3.add_trace(go.Scatter(x=provisiones.index, y=provisiones[provision], mode="lines", name=provision), row=row, col=col)

st.plotly_chart(fig3, use_container_width=True)

















