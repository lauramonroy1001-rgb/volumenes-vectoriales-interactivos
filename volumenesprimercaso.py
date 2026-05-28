import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Renderizador ultra-robusto para tu Jupyter local
pio.renderers.default = "browser"

# 1. Definir el radio r=4 (para r^2=16)
r = 4

# 2. Rejilla densa para superficies suaves
n = 60
puntos = np.linspace(-r, r, n)
X, Y, Z = np.meshgrid(puntos, puntos, puntos)

# 3. Intersección de SOLO DOS cilindros
cilindro_z = (X**2 + Y**2 <= r**2)  # Cilindro a lo largo de Z
cilindro_y = (X**2 + Z**2 <= r**2)  # Cilindro a lo largo de Y
# (Nota: Quitamos el cilindro x para que sea un bicilindro)

bicilindro = cilindro_z & cilindro_y
valores = bicilindro.astype(float)

# 4. Crear el volumen con Isosurface (caras suaves)
fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=valores.flatten(),
    isomin=0.5,
    isomax=1.0,
    surface_count=1,
    colorscale='Cividis',  # Cambié el color a azul/amarillo para diferenciarlo del tricilindro
    showscale=False,
    caps=dict(x_show=False, y_show=False, z_show=False)
))

# 5. Configurar diseño de la ventana 3D
fig.update_layout(
    title=r"Bicilindro Interactivo ($x^2+y^2 \leq 16$ e $x^2+z^2 \leq 16$)",
    scene=dict(
        xaxis=dict(title='Eje X', nticks=6, range=[-r, r]),
        yaxis=dict(title='Eje Y', nticks=6, range=[-r, r]),
        zaxis=dict(title='Eje Z', nticks=6, range=[-r, r]),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=40)
)

# Mostrar el gráfico
fig.show()