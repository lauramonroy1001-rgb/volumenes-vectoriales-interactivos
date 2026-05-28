import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(page_title="Volúmenes Vectoriales Interactivos", layout="wide")

st.title("Poliedros de Steinmetz: Intersección de Cilindros")
st.write("Modifica los parámetros en el panel de la izquierda para ver cómo cambia el volumen tridimensional.")

# ==========================================
# PANEL DE CONTROL (BARRA LATERAL)
# ==========================================
st.sidebar.header("Configuración del Modelo")

# 1. Selector de Caso
caso = st.sidebar.selectbox(
    "Selecciona el tipo de intersección:",
    ["Caso 1: Bicilindro (2 cilindros)", 
     "Caso 2: Tricilindro Simétrico (3 cilindros)", 
     "Caso 3: Tricilindro Asimétrico (Radios distintos)"]
)

# 2. Controles de Radio según el caso elegido
st.sidebar.subheader("Dimensiones (Radios)")
if caso == "Caso 1: Bicilindro (2 cilindros)":
    r = st.sidebar.slider("Radio de los cilindros (r)", min_value=1.0, max_value=6.0, value=4.0, step=0.5)
    lim = r
elif caso == "Caso 2: Tricilindro Simétrico (3 cilindros)":
    r = st.sidebar.slider("Radio de los 3 cilindros (r)", min_value=1.0, max_value=6.0, value=2.0, step=0.5)
    lim = r
else: # Caso 3: Asimétrico
    r_z = st.sidebar.slider("Radio Cilindro Z (Base en XY)", min_value=1.0, max_value=6.0, value=4.0, step=0.5)
    r_x = st.sidebar.slider("Radio Cilindro X (Base en YZ)", min_value=1.0, max_value=6.0, value=3.0, step=0.5)
    r_y = st.sidebar.slider("Radio Cilindro Y (Base en XZ)", min_value=1.0, max_value=6.0, value=2.0, step=0.5)
    lim = max(r_z, r_x, r_y)

# 3. Personalización Estética
st.sidebar.subheader("Estilo Visual")
paleta_color = st.sidebar.selectbox("Escala de colores:", ["Cividis", "Oranges", "Viridis", "Plasma", "Turbo"])
n = st.sidebar.slider("Suavidad de la superficie (Resolución de rejilla)", min_value=30, max_value=80, value=50, step=5)

# ==========================================
# CÁLCULOS MATEMÁTICOS Y LÓGICA BOOLEANA
# ==========================================
# Generar la rejilla 3D basada en el límite máximo necesario
puntos = np.linspace(-lim, lim, n)
X, Y, Z = np.meshgrid(puntos, puntos, puntos)

# Definición de las condiciones lógicas de los cilindros
if "Caso 1" in caso:
    cilindro_z = (X**2 + Y**2 <= r**2)
    cilindro_y = (X**2 + Z**2 <= r**2)
    volumen_logico = cilindro_z & cilindro_y
    titulo_grafico = f"Bicilindro Interactivo ($x^2+y^2 \leq {r**2:.1f}$ e $x^2+z^2 \leq {r**2:.1f}$)"

elif "Caso 2" in caso:
    cilindro_z = (X**2 + Y**2 <= r**2)
    cilindro_x = (Y**2 + Z**2 <= r**2)
    cilindro_y = (X**2 + Z**2 <= r**2)
    volumen_logico = cilindro_z & cilindro_x & cilindro_y
    titulo_grafico = f"Tricilindro Simétrico Interactivo (r={r})"

else: # Caso 3: Asimétrico
    cilindro_z = (X**2 + Y**2 <= r_z**2)
    cilindro_x = (Y**2 + Z**2 <= r_x**2)
    cilindro_y = (X**2 + Z**2 <= r_y**2)
    volumen_logico = cilindro_z & cilindro_x & cilindro_y
    titulo_grafico = f"Tricilindro Asimétrico: $x^2+y^2<{r_z**2:.0f}$, $y^2+z^2<{r_x**2:.0f}$, $x^2+z^2<{r_y**2:.0f}$"

valores = volumen_logico.astype(float)

# ==========================================
# RENDERIZADO DEL GRÁFICO 3D
# ==========================================
fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=valores.flatten(),
    isomin=0.5,
    isomax=1.0,
    surface_count=1,
    colorscale=paleta_color,
    showscale=False,
    caps=dict(x_show=False, y_show=False, z_show=False)
))

fig.update_layout(
    title=titulo_grafico,
    scene=dict(
        xaxis=dict(title='Eje X', nticks=6, range=[-lim, lim]),
        yaxis=dict(title='Eje Y', nticks=6, range=[-lim, lim]),
        zaxis=dict(title='Eje Z', nticks=6, range=[-lim, lim]),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=40),
    height=650
)

# Mostrar el gráfico en la interfaz de Streamlit
st.plotly_chart(fig, use_container_width=True)

# Sección informativa adicional para el usuario en la app
st.info("💡 **Consejo:** Puedes usar el ratón dentro del gráfico para rotar el volumen, hacer zoom y examinar las caras de la intersección.")
