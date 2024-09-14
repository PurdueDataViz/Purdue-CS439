import numpy as np
import matplotlib.pyplot as plt

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]
colors = [[1,0,0], [0,0,1], [1,0.5,0], [0,1,0], [1,1,0]]

fig, axs = plt.subplots()
axs.bar(fruits, counts, width=0.9)
plt.show()
