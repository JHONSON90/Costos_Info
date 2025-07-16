import streamlit as st

ADMIN_EMAILS = ["costosproinsalud@gmail.com", "edisonportillal@gmail.com"]

st.set_page_config(
    page_title="Costos Proinsalud",
    page_icon=":hospital:",
    layout="wide")

def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login)

if not st.user.is_logged_in:
    #pg = st.navigation([st.Page(login_screen)])
    login_screen()
    st.stop()

else:
    if st.user.email in ADMIN_EMAILS:
        st.session_state.role = "admin"
    else:
        st.session_state.role = "user"

    st.sidebar.header(f"Bienvenido, {st.user.name}!")
    st.sidebar.button("Cerrar sesión", on_click=st.logout)

    gastos = st.Page("gastos/gastos_info.py", title="Gastos Generales")
    nomina = st.Page("nomina/nomina_info.py", title="Nomina")
    medicamentos = st.Page("medicamentos/medicamentos_info.py", title="Medicamentos")
    honorarios =st.Page("honorarios/honorarios_info.py", title="Honorarios")
    costos =st.Page("informe_costos/costos_info.py", title="Informe de Costos")
    cuentas_medicas = st.Page("cuentas_medicas/cuentas_medicas.py", title="Cuentas Medicas")
    administrador = st.Page("administrador/admon.py", title="Administrador")

    admon_pages = [gastos, nomina, medicamentos, honorarios, costos, cuentas_medicas, administrador]
    user_pages = [gastos, nomina, medicamentos, honorarios, costos, cuentas_medicas]

    page_dict = admon_pages if st.session_state.role == "admin" else user_pages
    pg = st.navigation(page_dict)

pg.run()