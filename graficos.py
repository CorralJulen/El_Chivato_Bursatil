import matplotlib.pyplot as plt

def crear_grafico_lineas(df):
    """
    Recibe un DataFrame y pinta una gráfica de líneas usando Matplotlib.
    Esta es la forma clásica que enseñan en la universidad.
    """
    # Creamos el "Lienzo" (fig) y los "Ejes" (ax)
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Pintamos los datos
    ax.plot(df.index, df, label=df.columns)
    
    # Decoración (Título, etiquetas, rejilla...)
    ax.set_title("Evolución del Precio")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (€/$)")
    ax.legend() # Muestra la leyenda (ej: BBVA.MC)
    ax.grid(True) # Pone la cuadrícula de fondo
    
    return fig