import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Parche obligatorio para que se vea en tu versión de Jupyter
pio.renderers.default = "browser"

# 1. Definir el radio r=2
r = 2

# 2. Rejilla densa para suavidad
n = 60
puntos = np.linspace(-r, r, n)
X, Y, Z = np.meshgrid(puntos, puntos, puntos)

# 3. Intersección de los 3 cilindros
cilindro_z = (X**2 + Y**2 <= r**2)
cilindro_x = (Y**2 + Z**2 <= r**2)
cilindro_y = (X**2 + Z**2 <= r**2)

tricilindro = cilindro_z & cilindro_x & cilindro_y
valores = tricilindro.astype(float)

# 4. Crear el volumen con Isosurface (caras suaves)
fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=valores.flatten(),
    isomin=0.5,
    isomax=1.0,
    surface_count=1,
    colorscale='Oranges',
    showscale=False,
    caps=dict(x_show=False, y_show=False, z_show=False)
))

# 5. Configurar diseño de la ventana 3D
fig.update_layout(
    title=f"Tricilindro Interactivo (r={r})",
    scene=dict(
        xaxis=dict(nticks=6, range=[-r, r]),
        yaxis=dict(nticks=6, range=[-r, r]),
        zaxis=dict(nticks=6, range=[-r, r]),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=40)
)

# Mostrar el gráfico
fig.show()