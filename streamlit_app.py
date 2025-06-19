import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# st.write("Hello World")

# st.button("Click Me")

# if st.button("decir Hola"):
#     st.write("Hola")
# else:
#     st.write("Adios")

# st.write("Diferentes formas de usar write")

# st.write('Hello, *World!* :gafas:')

# st.write(1234)

# df = pd.DataFrame({
#      'first column': [1, 2, 3, 4],
#      'second column': [10, 20, 30, 40]
#      })
# st.write(df)

# st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

# df2 = pd.DataFrame(
#      np.random.randn(200, 3),
#      columns=['a', 'b', 'c'])
# c = alt.Chart(df2).mark_circle().encode(
#      x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# st.write(c)


# from datetime import time, datetime

# st.header('st.slider')

# # Ejemplo 1

# st.subheader('Slider')

# age = st.slider('How old are you?', 0, 100, 30)
# st.write("I'm ", age, 'years old')

# # Ejemplo 2

# st.subheader('Range slider')

# values = st.slider(
#      'Select a range of values',
#      0.0, 100.0, (25.0, 75.0))
# st.write('Values:', values)

# # Ejemplo 3

# st.subheader('Range time slider')

# appointment = st.slider(
#      "Schedule your appointment:",
#      value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)

# # Ejemplo 4

# st.subheader('Datetime slider')

# start_time = st.slider(
#      "When do you start?",
#      value=datetime(2020, 1, 1, 9, 30),
#      format="MM/DD/YY - hh:mm")
# st.write("Start time:", start_time)


# st.header('Line chart')

# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])

# st.line_chart(chart_data)

# st.header('st.selectbox')

# option = st.selectbox(
#      'What is your favorite color?',
#      ('Blue', 'Red', 'Green'))

# st.write('Your favorite color is ', option)


# st.header('st.multiselect')

# options = st.multiselect(
#      'What are your favorite colors',
#      ['Green', 'Yellow', 'Red', 'Blue'],
#      ['Yellow', 'Red'])

# st.write('You selected:', options)


# st.header('st.checkbox')

# st.write ('What would you like to order?')

# icecream = st.checkbox('Ice cream')
# coffee = st.checkbox('Coffee')
# cola = st.checkbox('Cola')

# if icecream:
#      st.write("Great! Here's some more 🍦")

# if coffee: 
#      st.write("Okay, here's some coffee ☕")

# if cola:
#      st.write("Here you go 🥤")

# #no deja instalar el streamlit_pandas_profiling
# # from streamlit_pandas_profiling import st_profile_report

# # st.header('`streamlit_pandas_profiling`')

# # df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv')

# # pr = df.profile_report()
# # st_profile_report(pr)


# st.header('st.latex')

# st.latex(r'''
#      a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
#      \sum_{k=0}^{n-1} ar^k =
#      a \left(\frac{1-r^{n}}{1-r}\right)
#      ''')

# st.latex("sumar")


# st.title('Customizing the theme of Streamlit apps')

# st.write('Contents of the `.streamlit/config.toml` file of this app')

# st.code("""
# [theme]
# primaryColor="#F39C12"
# backgroundColor="#2E86C1"
# secondaryBackgroundColor="#AED6F1"
# textColor="#FFFFFF"
# font="monospace"
# """)

# number = st.sidebar.slider('Select a number:', 0, 10, 5)
# st.write('Selected number from slider widget is:', number)

# # st.title('st.secrets')

# # st.write(st.secrets['message'])

# st.title('st.file_uploader')

# st.subheader('Input CSV')
# uploaded_file = st.file_uploader("Choose a file")

# if uploaded_file is not None:
#   df = pd.read_csv(uploaded_file)
#   st.subheader('DataFrame')
#   st.write(df)
#   st.subheader('Descriptive Statistics')
#   st.write(df.describe())
# else:
#   st.info('☝️ Upload a CSV file')

# st.set_page_config(layout="wide")

# st.title('How to layout your Streamlit app')

# with st.expander('About this app'):
#   st.write('This app shows the various ways on how you can layout your Streamlit app.')
#   st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

# st.sidebar.header('Input')
# user_name = st.sidebar.text_input('What is your name?')
# user_emoji = st.sidebar.selectbox('Choose an emoji', ['', '😄', '😆', '😊', '😍', '😴', '😕', '😱'])
# user_food = st.sidebar.selectbox('What is your favorite food?', ['', 'Tom Yum Kung', 'Burrito', 'Lasagna', 'Hamburger', 'Pizza'])

# st.header('Output')

# col1, col2, col3 = st.columns(3)

# with col1:
#   if user_name != '':
#     st.write(f'👋 Hello {user_name}!')
#   else:
#     st.write('👈  Please enter your **name**!')

# with col2:
#   if user_emoji != '':
#     st.write(f'{user_emoji} is your favorite **emoji**!')
#   else:
#     st.write('👈 Please choose an **emoji**!')

# with col3:
#   if user_food != '':
#     st.write(f'🍴 **{user_food}** is your favorite **food**!')
#   else:
#     st.write('👈 Please choose your favorite **food**!')


# import time

# st.title('st.progress')

# with st.expander('About this app'):
#      st.write('You can now display the progress of your calculations in a Streamlit app with the `st.progress` command.')

# my_bar = st.progress(0)

# for percent_complete in range(100):
#      time.sleep(0.05)
#      my_bar.progress(percent_complete + 1)

# st.balloons()

# st.title('st.form')

# # Full example of using the with notation
# st.header('1. Example of using `with` notation')
# st.subheader('Coffee machine')

# with st.form('my_form'):
#     st.write('**Order your coffee**')

#     # Input widgets
#     coffee_bean_val = st.selectbox('Coffee bean', ['Arabica', 'Robusta'])
#     coffee_roast_val = st.selectbox('Coffee roast', ['Light', 'Medium', 'Dark'])
#     brewing_val = st.selectbox('Brewing method', ['Aeropress', 'Drip', 'French press', 'Moka pot', 'Siphon'])
#     serving_type_val = st.selectbox('Serving format', ['Hot', 'Iced', 'Frappe'])
#     milk_val = st.select_slider('Milk intensity', ['None', 'Low', 'Medium', 'High'])
#     owncup_val = st.checkbox('Bring own cup')

#     # Every form must have a submit button
#     submitted = st.form_submit_button('Submit')

# if submitted:
#     st.markdown(f'''
#         ☕ You have ordered:
#         - Coffee bean: `{coffee_bean_val}`
#         - Coffee roast: `{coffee_roast_val}`
#         - Brewing: `{brewing_val}`
#         - Serving type: `{serving_type_val}`
#         - Milk: `{milk_val}`
#         - Bring own cup: `{owncup_val}`
#         ''')
# else:
#     st.write('☝️ Place your order!')


# # Short example of using an object notation
# st.header('2. Example of object notation')

# form = st.form('my_form_2')
# selected_val = form.slider('Select a value')
# form.form_submit_button('Submit')

# st.write('Selected value: ', selected_val)


# # st.title('st.experimental_get_query_params')

# # with st.expander('About this app'):
# #   st.write("`st.experimental_get_query_params` allows the retrieval of query parameters directly from the URL of the user's browser.")

# # # 1. Instructions
# # st.header('1. Instructions')
# # st.markdown('''
# # In the above URL bar of your internet browser, append the following:
# # `?name=Jack&surname=Beanstalk`
# # after the base URL `http://share.streamlit.io/dataprofessor/st.experimental_get_query_params/`
# # such that it becomes 
# # `http://share.streamlit.io/dataprofessor/st.experimental_get_query_params/?firstname=Jack&surname=Beanstalk`
# # ''')


# # # 2. Contents of st.experimental_get_query_params
# # st.header('2. Contents of st.experimental_get_query_params')
# # st.write(st.experimental_get_query_params())


# # # 3. Retrieving and displaying information from the URL
# # st.header('3. Retrieving and displaying information from the URL')

# # firstname = st.experimental_get_query_params()['firstname'][0]
# # surname = st.experimental_get_query_params()['surname'][0]

# # st.write(f'Hello **{firstname} {surname}**, how are you?')


# from time import time
# st.title('st.cache')

# # Using cache
# a0 = time()
# st.subheader('Using st.cache')

# @st.cache(suppress_st_warning=True)
# def load_data_a():
#   df = pd.DataFrame(
#     np.random.rand(2000000, 5),
#     columns=['a', 'b', 'c', 'd', 'e']
#   )
#   return df

# st.write(load_data_a())
# a1 = time()
# st.info(a1-a0)


# # Not using cache
# b0 = time()
# st.subheader('Not using st.cache')

# def load_data_b():
#   df = pd.DataFrame(
#     np.random.rand(2000000, 5),
#     columns=['a', 'b', 'c', 'd', 'e']
#   )
#   return df

# st.write(load_data_b())
# b1 = time()
# st.info(b1-b0)

# st.title('st.session_state')

# def lbs_to_kg():
#   st.session_state.kg = st.session_state.lbs/2.2046
# def kg_to_lbs():
#   st.session_state.lbs = st.session_state.kg*2.2046

# st.header('Input')
# col1, spacer, col2 = st.columns([2,1,2])
# with col1:
#   pounds = st.number_input("Pounds:", key = "lbs", on_change = lbs_to_kg)
# with col2:
#   kilogram = st.number_input("Kilograms:", key = "kg", on_change = kg_to_lbs)

# st.header('Output')
# st.write("st.session_state object:", st.session_state)



# # import requests


# # st.title('🏀 Bored API app')

# # st.sidebar.header('Input')
# # selected_type = st.sidebar.selectbox('Select an activity type', ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])

# # suggested_activity_url = f'http://www.boredapi.com/api/activity?type={selected_type}'
# # json_data = requests.get(suggested_activity_url)
# # #suggested_activity = json_data.json()

# # if json_data.status_code == 200:
# #     try:
# #         suggested_activity = json_data.json()
# #         with st.expander('Suggested activity'):
# #             st.write(':point_right:', suggested_activity['activity'])
# #             st.write('Number of participants:', suggested_activity['participants'])
# #             st.write('Type of activity:', suggested_activity['type'])
# #             st.write('Price:', suggested_activity['price'])
# #             st.write('Link:', suggested_activity['link'])
# #             st.write('Key:', suggested_activity['key'])
# #             st.write('Accessibility:', suggested_activity['accessibility'])
# #     except json.JSONDecodeError:
# #         st.error("Error al procesar la respuesta de la API")
# #         st.write(f"Contenido recibido: {json_data.text}")
# # else:
# #     st.error(f"Error al obtener la actividad: {json_data.status_code}")

# # # Agregar un botón para obtener una nueva actividad
# # if st.button('Get another activity'):
# #     json_data = requests.get(suggested_activity_url)
# #     if json_data.status_code == 200:
# #         try:
# #             suggested_activity = json_data.json()
# #             with st.expander('Suggested activity'):
# #                 st.write(':point_right:', suggested_activity['activity'])
# #                 st.write('Number of participants:', suggested_activity['participants'])
# #                 st.write('Type of activity:', suggested_activity['type'])
# #                 st.write('Price:', suggested_activity['price'])
# #                 st.write('Link:', suggested_activity['link'])
# #                 st.write('Key:', suggested_activity['key'])
# #                 st.write('Accessibility:', suggested_activity['accessibility'])
# #         except json.JSONDecodeError:
# #             st.error("Error al procesar la respuesta de la API")
# #             st.write(f"Contenido recibido: {json_data.text}")
# #     else:
# #         st.error(f"Error al obtener la actividad: {json_data.status_code}")

# # c1, c2 = st.columns(2)
# # with c1:
# #   with st.expander('About this app'):
# #     st.write('Are you bored? The **Bored API app** provides suggestions on activities that you can do when you are bored. This app is powered by the Bored API.')
# # with c2:
# #   with st.expander('JSON data'):
# #     st.write(suggested_activity_url)

# # st.header('Suggested activity')
# # st.info(suggested_activity['activity'])

# # col1, col2, col3 = st.columns(3)
# # with col1:
# #   st.metric(label='Number of Participants', value=suggested_activity['participants'], delta='')
# # with col2:
# #   st.metric(label='Type of Activity', value=suggested_activity['type'].capitalize(), delta='')
# # with col3:
# #   st.metric(label='Price', value=suggested_activity['price'], delta='')


# import json
# from pathlib import Path

# # En cuanto a Streamlit Elements, necesitaremos todos estos objetos.
# # Todos los objetos disponibles y su uso se enumeran aquí: https://github.com/okld/streamlit-elements#getting-started

# from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# # Cambie el diseño de la página para que el tablero ocupe toda la página.

# st.set_page_config(layout="wide")

# with st.sidebar:
#     st.title("🗓️ #30DaysOfStreamlit")
#     st.header("Day 27 - Streamlit Elements")
#     st.write("Build a draggable and resizable dashboard with Streamlit Elements.")
#     st.write("---")

#     # Define URL for media player.
#     media_url = st.text_input("Media URL", value="https://www.youtube.com/watch?v=vIQQR_yq-8I")

# # Inicialice los datos predeterminados para el editor de código y el gráfico.
# #
# # Para este tutorial, necesitaremos datos para un gráfico Nivo Bump.
# # Puede obtener datos aleatorios aquí, en la pestaña 'datos': https://nivo.rocks/bump/
# #
# # Como verá a continuación, este elemento de estado de sesión se actualizará cuando nuestro
# # editor de código cambie, y el gráfico Nivo Bump lo leerá para dibujar los datos.

# if "data" not in st.session_state:
#     st.session_state.data = Path("data.json").read_text()

# # Defina un diseño de tablero predeterminado.
# # La grilla tiene 12 columnas por defecto.
# #
# # Para obtener más información sobre los parámetros disponibles:
# # https://github.com/react-grid-layout/react-grid-layout#grid-item-props

# layout = [
#     # El elemento del editor se coloca en las coordenadas x=0 e y=0, ocupa 6/12 columnas y tiene una altura de 3.
#     dashboard.Item("editor", 0, 0, 6, 3),
#     # El elemento del gráfico se coloca en las coordenadas x=6 e y=0, ocupa 6/12 columnas y tiene una altura de 3.
#     dashboard.Item("chart", 6, 0, 6, 3),
#     # El elemento multimedia se coloca en las coordenadas x=0 e y=3, ocupa 6/12 columnas y tiene una altura de 4.
#     dashboard.Item("media", 0, 2, 12, 4),
# ]

# # Crea un marco para mostrar elementos.

# with elements("demo"):

#     # Cree un nuevo panel con el diseño especificado anteriormente.
#     #
#     # draggableHandle es un selector de CSS que define la parte que se puede arrastrar de cada elemento del tablero.
#     # Aquí, los elementos con un nombre de clase 'draggable' serán arrastrables.
#     #
#     # Para obtener más información sobre los parámetros disponibles:
#     # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
#     # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

#     with dashboard.Grid(layout, draggableHandle=".draggable"):

#         # Primera tarjeta, el editor de código.
#         #
#         # Utilizamos el parámetro `key` para identificar el elemento correcto
#         #
#         # Para hacer que el contenido de la tarjeta llene automáticamente la altura disponible, usaremos CSS flexbox.
#         # sx es un parámetro disponible con cada componente de Material UI para definir atributos CSS.
#         #
#         # Para más información sobre Card, flexbox y sx:
#         # https://mui.com/components/cards/
#         # https://mui.com/system/flexbox/
#         # https://mui.com/system/the-sx-prop/

#         with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

#             # Para hacer que este encabezado se pueda arrastrar, solo necesitamos establecer su nombre de clase en 'draggable',
#             # como se definió anteriormente en dashboard.Grid's draggableHandle.

#             mui.CardHeader(title="Editor", className="draggable")

#             # Queremos hacer que el contenido de la tarjeta tome toda la altura disponible configurando el valor de CSS flex en 1.
#             # También queremos que el contenido de la tarjeta se reduzca cuando la tarjeta se encoja al establecer minHeight en 0.

#             with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

#                 # Aquí está nuestro editor de código de Monaco.
#                 #
#                 # Primero, establecemos el valor predeterminado en st.session_state.data que inicializamos anteriormente.
#                 # Segundo, definimos el lenguaje a usar, JSON.
#                 #
#                 # Luego, queremos recuperar los cambios realizados en el contenido del editor.
#                 # Al verificar la documentación de Monaco, hay una propiedad onChange que toma una función.
#                 # Esta función se llama cada vez que se realiza un cambio, y el valor del contenido actualizado se pasa en
#                 # el primer parámetro (onChange: https://github.com/suren-atoyan/monaco-react#props)
#                 #
#                 # Streamlit Elements proveé una función especial sync(). Esta función crea un Callback y
#                 # automáticamente redirecciona sus parámetros al estado de sesión de Streamlit.
#                 #
#                 # Ejemplos
#                 # --------
#                 # Cree un Callback que reenvíe su primer parámetro a un elemento del estado de sesión llamado "data":
#                 # >>> editor.Monaco(onChange=sync("data"))
#                 # >>> print(st.session_state.data)
#                 #
#                 # Cree un Callback que reenvíe su segundo parámetro a un elemento del estado de sesión llamado "ev":
#                 # >>> editor.Monaco(onChange=sync(None, "ev"))
#                 # >>> print(st.session_state.ev)
#                 #
#                 # Cree un Callback que reenvíe sus dos parámetros al estado:
#                 # >>> editor.Monaco(onChange=sync("data", "ev"))
#                 # >>> print(st.session_state.data)
#                 # >>> print(st.session_state.ev)
#                 #
#                 # Ahora, hay un problema: se llama a onChange cada vez que se realiza un cambio, lo que significa que cada vez
#                 # que escribe un solo carácter, toda su aplicación Streamlit se volverá a ejecutar.
#                 #
#                 # Para evitar este problema, puede decirle a Streamlit Elements que espere a que ocurra otro evento
#                 # (como un clic de botón) para enviar los datos actualizados, envolviendo su devolución de llamada con lazy().
#                 #
#                 # Para obtener más información sobre Monaco:
#                 # https://github.com/suren-atoyan/monaco-react
#                 # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

#                 editor.Monaco(
#                     defaultValue=st.session_state.data,
#                     language="json",
#                     onChange=lazy(sync("data"))
#                 )

#             with mui.CardActions:

#                 # Monaco editor tiene un Lazy Callback atado al onChange, lo que significa que incluso si cambias
#                 # el contenido de Monaco, Streamlit no va a ser notificado directamente, lo que previene que se recargue todo el tiempo.
#                 # Entonces necesitamos otro evento para iniciar la actualización.
#                 #
#                 # La solución es crear un botón que dispare un Callback al hacer click.
#                 # 
#                 # Nuestro callback no necesita hacer nada en particular. Tu puedes incluso crear una
#                 # función vacía de Python, o utilizar sync() sin ningún argumento.
#                 #
#                 # Ahora, cada vez que hagas click en ese botón, el callback de onClick va a ser iniciado, pero
#                 # cualquier otro lazy callback que cambió va a ser también llamado. 

#                 mui.Button("Apply changes", onClick=sync())

#         # Segunda tarjeta, el gráfico Nivo Bump.
#         # Usaremos la misma configuración de flexbox que la primera tarjeta para ajustar automáticamente la altura del contenido.

#         with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

#             # Para hacer que este encabezado se pueda arrastrar, solo necesitamos establecer su nombre de clase en 'draggable',
#             # como se definió anteriormente en dashboard.Grid's draggableHandle.

#             mui.CardHeader(title="Chart", className="draggable")

#             # Como arriba, queremos que nuestro contenido crezca y se reduzca a medida que el usuario cambia el tamaño de la tarjeta,
#             # configurando flex en 1 y minHeight en 0.

#             with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

#                 # Aquí es donde dibujaremos nuestro gráfico Bump.
#                 #
#                 # Para este ejercicio, podemos simplemente adaptar el ejemplo de Nivo y hacer que funcione con Streamlit Elements.
#                 # El ejemplo de Nivo está disponible en la pestaña 'code': https://nivo.rocks/bump/
#                 #
#                 # Los datos toman un diccionario como parámetro, por lo que necesitamos convertir nuestros datos JSON de una cadena a
#                 # un diccionario Python, con `json.loads()`.
#                 #
#                 # Para obtener más información sobre Nivo:
#                 # https://nivo.rocks/

#                 nivo.Bump(
#                     data=json.loads(st.session_state.data),
#                     colors={ "scheme": "spectral" },
#                     lineWidth=3,
#                     activeLineWidth=6,
#                     inactiveLineWidth=3,
#                     inactiveOpacity=0.15,
#                     pointSize=10,
#                     activePointSize=16,
#                     inactivePointSize=0,
#                     pointColor={ "theme": "background" },
#                     pointBorderWidth=3,
#                     activePointBorderWidth=3,
#                     pointBorderColor={ "from": "serie.color" },
#                     axisTop={
#                         "tickSize": 5,
#                         "tickPadding": 5,
#                         "tickRotation": 0,
#                         "legend": "",
#                         "legendPosition": "middle",
#                         "legendOffset": -36
#                     },
#                     axisBottom={
#                         "tickSize": 5,
#                         "tickPadding": 5,
#                         "tickRotation": 0,
#                         "legend": "",
#                         "legendPosition": "middle",
#                         "legendOffset": 32
#                     },
#                     axisLeft={
#                         "tickSize": 5,
#                         "tickPadding": 5,
#                         "tickRotation": 0,
#                         "legend": "ranking",
#                         "legendPosition": "middle",
#                         "legendOffset": -40
#                     },
#                     margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
#                     axisRight=None,
#                 )

#         # Tercer elemento del tablero, el reproductor multimedia.

#         with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):
#             mui.CardHeader(title="Media Player", className="draggable")
#             with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

#                 # Este elemento funciona con ReactPlayer, es compatible con muchos otros reproductores
#                 # además de YouTube. Puedes verificarlo aquí: https://github.com/cookpete/react-player#props

#                 media.Player(url=media_url, width="100%", height="100%", controls=True)

st.title('🖼️ yt-img-app')
st.header('YouTube Thumbnail Image Extractor App')

with st.expander('About this app'):
  st.write('This app retrieves the thumbnail image from a YouTube video.')

# Image settings
st.sidebar.header('Settings')
img_dict = {'Max': 'maxresdefault', 'High': 'hqdefault', 'Medium': 'mqdefault', 'Standard': 'sddefault'}
selected_img_quality = st.sidebar.selectbox('Select image quality', ['Max', 'High', 'Medium', 'Standard'])
img_quality = img_dict[selected_img_quality]

yt_url = st.text_input('Paste YouTube URL', 'https://youtu.be/JwSS70SZdyM')

def get_ytid(input_url):
  if 'youtu.be' in input_url:
    ytid = input_url.split('/')[-1]
  if 'youtube.com' in input_url:
    ytid = input_url.split('=')[-1]
  return ytid

# Display YouTube thumbnail image
if yt_url != '':
  ytid = get_ytid(yt_url) # yt or yt_url

  yt_img = f'http://img.youtube.com/vi/{ytid}/{img_quality}.jpg'
  st.image(yt_img)
  st.write('YouTube video thumbnail image URL: ', yt_img)
else:
  st.write('☝️ Enter URL to continue ...')