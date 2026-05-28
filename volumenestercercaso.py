import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Renderizador ultra-robusto para tu Jupyter local
pio.renderers.default = "browser"

# 1. El radio máximo manda para definir el tamaño de la caja (r=4)
lim = 4

# 2. Rejilla densa para superficies suaves
n = 70
puntos = np.linspace(-lim, lim, n)
X, Y, Z = np.meshgrid(puntos, puntos, puntos)

# 3. Ecuaciones con sus respectivos radios cuadrados (<16, <9, <4)
cilindro_z = (X**2 + Y**2 <= 16)  # Radio 4 (A lo largo de Z)
cilindro_x = (Y**2 + Z**2 <= 9)   # Radio 3 (A lo largo de X)
cilindro_y = (X**2 + Z**2 <= 4)   # Radio 2 (A lo largo de Y)

# Intersección de los tres cilindros desiguales
tricilindro_asym = cilindro_z & cilindro_x & cilindro_y
valores = tricilindro_asym.astype(float)

# 4. Crear el volumen con Isosurface (caras suaves)
fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=valores.flatten(),
    isomin=0.5,
    isomax=1.0,
    surface_count=1,
    colorscale='Viridis',  # Escala de color llamativa para resaltar la asimetría
    showscale=False,
    caps=dict(x_show=False, y_show=False, z_show=False)
))

# 5. Configurar diseño de la ventana 3D
fig.update_layout(
    title="Tricilindro Asimétrico: $x^2+y^2<16$, $y^2+z^2<9$, $x^2+z^2<4$",
    scene=dict(
        xaxis=dict(title='Eje X', nticks=6, range=[-lim, lim]),
        yaxis=dict(title='Eje Y', nticks=6, range=[-lim, lim]),
        zaxis=dict(title='Eje Z', nticks=6, range=[-lim, lim]),
        aspectmode='cube'
    ),
    margin=dict(r=0, l=0, b=0, t=40)
)

# Mostrar el gráfico
fig.show()