import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(-5.0*np.pi, 5.0*np.pi, 0.01)
s = np.sin(t)/t

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='x', ylabel='sin(x)/x',
       title='Sinc function')
ax.grid()

fig.savefig("sinc.png")
plt.show()
