import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(-5*math.pi, 5*math.pi, 200)
# print(x)
y = [ math.sin(u)/u for u in x ]

plt.plot(x, y)
plt.show()