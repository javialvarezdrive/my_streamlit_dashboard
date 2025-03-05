import streamlit as st
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import URL
import plotly.express as px

# Configuración de Streamlit
st.set_page_config(
    page_title="Dashboard de Actividades",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar datos desde Supabase
@st.cache_data(ttl=600)
def cargarDatos(query):
    conString = st.secrets["conString"]
    engine = sa.create_engine(conString)
    df = pd.read_sql_query(query, engine)
    return df

# Función para ejecutar comandos SQL en Supabase (CRUD)
def ejecutarComandos(query):
    conString = st.secrets["conString"]
    engine = sa.create_engine(conString)
    with engine.connect() as connection:
        connection.execute(query)

# Cargar actividades y mostrar en el dashboard
st.title("Dashboard de Actividades del Gimnasio")

# Consultas SQL para obtener actividades
query_actividades = """
SELECT * FROM public.activities
"""
df_actividades = cargarDatos(query_actividades)

# Mostrar los datos de actividades en una tabla
st.subheader("Actividades Disponibles")
st.dataframe(df_actividades)

# Graficar las actividades por turno
st.subheader("Distribución de Actividades por Turno")
fig = px.bar(df_actividades, x='shift', title="Actividades por Turno", labels={'shift': 'Turno'})
st.plotly_chart(fig, use_container_width=True)

# CRUD: Agregar nueva actividad
st.sidebar.header("Agregar Nueva Actividad")
with st.sidebar.form(key='add_activity_form'):
    nombre = st.text_input('Nombre de la Actividad')
    descripcion = st.text_area('Descripción')
    fecha = st.date_input('Fecha de la Actividad')
    hora_inicio = st.time_input('Hora de Inicio')
    hora_fin = st.time_input('Hora de Fin')
    turno = st.selectbox('Turno', ['Mañana', 'Tarde', 'Noche'])
    max_participantes = st.number_input('Máximo de Participantes', min_value=1)

    submit_button = st.form_submit_button("Agregar Actividad")

    if submit_button:
        query_insert = f"""
        INSERT INTO public.activities (name, description, date, start_time, end_time, shift, max_participants)
        VALUES ('{nombre}', '{descripcion}', '{fecha}', '{hora_inicio}', '{hora_fin}', '{turno}', {max_participantes});
        """
        ejecutarComandos(query_insert)
        st.success("Actividad agregada exitosamente")

# CRUD: Eliminar actividad
st.sidebar.header("Eliminar Actividad")
actividad_a_eliminar = st.sidebar.selectbox('Seleccione una actividad para eliminar', df_actividades['name'])
if st.sidebar.button("Eliminar Actividad"):
    query_delete = f"""
    DELETE FROM public.activities WHERE name = '{actividad_a_eliminar}';
    """
    ejecutarComandos(query_delete)
    st.success(f"Actividad '{actividad_a_eliminar}' eliminada exitosamente")

