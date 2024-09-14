import numpy as np
import matplotlib.pyplot as plt

N = 400
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]

fig, ax = plt.subplots()
ax.scatter(x, y, c=colors, s=25*radii, alpha=0.5)

ax.set_xlabel('x', fontsize=15)
ax.set_ylabel('y', fontsize=15)
ax.set_title('Colored scatter plot')

ax.grid(True)
fig.tight_layout()

plt.show()
