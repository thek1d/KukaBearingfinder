import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

def animate(i):
    
    data = pd.read_csv('forces.csv')
    ts = data['Timestamp']
    forcex = data['Force_X']
    forcey = data['Force_Y']
    forcez = data['Force_Z']

    ax1.cla()
    ax1.plot(ts, forcex, label='Force x-Axis')
    ax1.plot(ts, forcey, label='Force y-Axis')
    ax1.plot(ts, forcez, label='Force z-Axis')
    ax1.set_title('Forces')
    ax1.set_xlabel('time [ms]')
    ax1.set_ylabel('force [N]')
    ax1.legend(loc='lower left')

    torqex = data['Torqe_X']
    torqey = data['Torqe_Y']
    torqez = data['Torqe_Z']

    ax2.cla()
    ax2.plot(ts, torqex, label='Torqe x-Axis')
    ax2.plot(ts, torqey, label='Torqe y-Axis')
    ax2.plot(ts, torqez, label='Torqe z-Axis')
    ax2.set_title('Torqes')
    ax2.set_xlabel('time [ms]')
    ax2.set_ylabel('torqe [Nmm]')
    ax2.legend(loc='lower left')

    plt.tight_layout()

ani  = FuncAnimation(fig, animate, interval=40)

plt.tight_layout()
plt.show()