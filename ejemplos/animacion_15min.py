import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from oleaje_operator import OleajeOperator

operador = OleajeOperator()
t = np.linspace(0, 900, 900)  # 15 minutos simulados

def animate(t, frames=900, interval=1000, threshold=2.5):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('black')
    ax.set_xlim(t[0], t[-1])
    ax.set_ylim(-3, 4)
    ax.set_title('🌊 Oleaje animado durante 15 minutos', fontsize=16)
    ax.set_xlabel('Tiempo t (segundos)')
    ax.set_ylabel('Intensidad / Vibración')
    ax.grid(True, linestyle='--', alpha=0.5)

    line_agua, = ax.plot([], [], label='Agua A(t)', color='blue')
    line_aire, = ax.plot([], [], label='Aire V(t)', color='green')
    line_oleaje, = ax.plot([], [], label='Oleaje O(t)', color='white')
    puntos_evento = ax.scatter([], [], color='red', label='🌊 Eventos activados')
    ax.legend()

    def actualizar(frame):
        shift = frame
        A, V, O = operador.compute(t, shift)
        eventos = operador.detect_event(O, threshold)

        line_agua.set_data(t, A)
        line_aire.set_data(t, V)
        line_oleaje.set_data(t, O)
        if eventos is not None:
            puntos_evento.set_offsets(np.c_[t[eventos], O[eventos]])
        else:
            puntos_evento.set_offsets(np.empty((0, 2)))

        return line_agua, line_aire, line_oleaje, puntos_evento

    ani = animation.FuncAnimation(fig, actualizar, frames=frames, interval=interval, blit=True)
    plt.show()

animate(t)
