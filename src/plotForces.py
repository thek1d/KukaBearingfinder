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
    ax1.plot(ts, forcex, label='Fx')
    ax1.plot(ts, forcey, label='Fy')
    ax1.plot(ts, forcez, label='Fz')
    ax1.set_title('Forces')
    ax1.set_xlabel('time [ms]')
    ax1.set_ylabel('Force [N]')
    ax1.legend(loc='upper left')

    torquex = data['Torque_X']
    torquey = data['Torque_Y']
    torquez = data['Torque_Z']

    ax2.cla()
    ax2.plot(ts, torquex, label='Mx')
    ax2.plot(ts, torquey, label='My')
    ax2.plot(ts, torquez, label='Mz')
    ax2.set_title('Torques')
    ax2.set_xlabel('Time [ms]')
    ax2.set_ylabel('Torque [Nmm]')
    ax2.legend(loc='upper left')

    plt.tight_layout()

ani  = FuncAnimation(fig, animate, interval=40)

plt.tight_layout()
plt.grid()
plt.show()
