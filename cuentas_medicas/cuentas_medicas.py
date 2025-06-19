
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import traceback
import time
import pandas as pd
import numpy as np



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
df.columns = df.columns.str.strip()

df["FECHA"] = pd.to_datetime(df["FECHA"], format="%Y/%m/%d")
df["DEBITOS"] = pd.to_numeric(df["DEBITOS"], errors='coerce')
df["CREDITOS"] = pd.to_numeric(df["CREDITOS"], errors='coerce')
df["SALDO"] = df["DEBITOS"] - df["CREDITOS"]

df["Mes"] = df["FECHA"].dt.month
df["Ano"] = df["FECHA"].dt.year

primer_trimestre = df.loc[df["FECHA"] > "2024-12-31"]

st.bar_chart(primer_trimestre, x="Correccion 1", y="CREDITOS")

correccion = primer_trimestre.groupby("Correccion 1")["CREDITOS"].sum()

st.write(correccion)    

proveedores = primer_trimestre.pivot_table(index="Nombre Proveedor", columns="Mes", values="CREDITOS", aggfunc="sum")
proveedores = proveedores.fillna(0)
proveedores["Total"] = proveedores.sum(axis=1)
st.write(proveedores)



