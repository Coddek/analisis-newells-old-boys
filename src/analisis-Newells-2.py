import pandas as pd
import plotly.express as px
from plotly import graph_objects as go

# Archivo src/main.py
from utils import cargar_datos, agrupar_datos

path = r'C:\Program Files (x86)\Coddek\ANALISIS DE DATOS TRABAJOS\analisis-newells-old-boys\data\futbolargentino_limpio.xlsx'

df = pd.read_excel(path)
"""
print("-"*20)
print(df.columns)
print("-"*20)
print(df.info)
print("-"*20)
print(df.nunique)"""


# Filtrar los jugadores que pertenecen a Newell's
df_newells = df[df['Club'] == "Newell's Old Boys"]

# Asegurarse de que 'Valor de mercado' esté en formato numérico
df_newells['Valor de mercado'] = pd.to_numeric(df_newells['Valor de mercado'], errors='coerce')

# Agrupar datos por temporada
jugadores_por_temporada = df_newells.groupby(['Temporada'])['Jugadores'].count().reset_index()
jugadores_caros_temporada = df_newells.groupby(['Temporada'])['Valor de mercado'].max().reset_index()
promedio_valor_temporada = df_newells.groupby(['Temporada'])['Valor de mercado'].mean().reset_index()

# Crear DataFrame para análisis
df_analisis = pd.DataFrame(columns=['Temporada', 'Jugadores', 'Valor Maximo de Mercado', 'Promedio de valor', 'Nombre Jugador mas caro'])
df_analisis['Temporada'] = jugadores_por_temporada['Temporada']
df_analisis['Jugadores'] = jugadores_por_temporada['Jugadores']
df_analisis['Valor Maximo de Mercado'] = jugadores_caros_temporada['Valor de mercado']
df_analisis['Promedio de valor'] = promedio_valor_temporada['Valor de mercado']

# Identificar el nombre del jugador más caro por temporada
for row, value in df_analisis.iterrows():
    df_analisis.at[row, 'Nombre Jugador mas caro'] = df_newells.loc[
        (df_newells['Valor de mercado'] == value['Valor Maximo de Mercado']) &
        (df_newells['Temporada'] == value['Temporada'])
    ].values[0][0]

# Crear el gráfico combinado con dos ejes Y
fig = go.Figure()

# Agregar barras para la cantidad de jugadores por temporada
fig.add_trace(go.Bar(
    x=df_analisis['Temporada'],
    y=df_analisis['Jugadores'],
    name='Jugadores por Temporada',
    marker=dict(color='rgba(0, 128, 255, 0.6)'),
    yaxis='y1'  # Asignar al primer eje Y
))

# Agregar una línea más visible para el promedio de valores de mercado
fig.add_trace(go.Scatter(
    x=df_analisis['Temporada'],
    y=df_analisis['Promedio de valor'],
    mode='lines+markers',
    name='Promedio Valor de Mercado',
    line=dict(color='red', width=6, dash='solid'),  # Grosor y estilo de la línea
    marker=dict(size=10, color='red'),
    yaxis='y2'  # Asignar al segundo eje Y
))

# Agregar marcadores para los jugadores más caros por temporada
fig.add_trace(go.Scatter(
    x=df_analisis['Temporada'],
    y=df_analisis['Valor Maximo de Mercado'],
    mode='markers+text',
    name='Jugador Más Caro',
    marker=dict(color='gold', size=14),
    text=df_analisis['Nombre Jugador mas caro'],
    textposition='top center',
    yaxis='y2'  # Asignar al segundo eje Y
))

# Configuración del diseño
fig.update_layout(
    title='Análisis de Newell\'s Old Boys por Temporada',
    xaxis_title='Temporada',
    yaxis=dict(
        title='Cantidad de Jugadores',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue'),
        side='left'
    ),
    yaxis2=dict(
        title='Valor de Mercado (en millones)',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        overlaying='y',
        side='right',
        range=[0, df_analisis['Valor Maximo de Mercado'].max() * 1.2],  # Más margen
        tickformat='.2s'  # Formato en "millones" (e.g., 1M, 2M)
    ),
    legend_title='Leyenda',
    template='plotly_white'
)

# Mostrar el gráfico
fig.show()

# Mostrar el DataFrame para análisis
print(df_analisis)


##### GRAFICO EDAD #######

# Asegurarse de que 'Edad' esté en formato numérico
df_newells['Edad'] = pd.to_numeric(df_newells['Edad'], errors='coerce')


edad_promedio_temporada = df_newells.groupby(['Temporada'])['Edad'].mean().reset_index()

graf_ext = px.bar (edad_promedio_temporada,
                   x='Temporada',
                   y='Edad',
                   title='Edad promedio por Temporada de Newells Old Boys',
                   labels={'Temporada': 'Temporada', 'Edad': 'Edad Promedio'},
                   color='Edad',  # Opcional, para resaltar las barras por su valor
                   color_continuous_scale='Viridis')  # Escala de color)

graf_ext.show()

# Mostrar el resultado
print(edad_promedio_temporada)