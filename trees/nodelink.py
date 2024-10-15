import numpy as np 
from matplotlib import pyplot as plt 
import matplotlib as mpl
import argparse 
import json 
from bigtree import Node, reingold_tilford, plot_tree
from bigtree.utils import iterators
import math

def import_tree_from_dict(nodeinfo, parent=None):
    anode = Node(name=nodeinfo['name'], value=0, 
                parent=parent, children=[])
    if 'value' in nodeinfo.keys():
        anode.value = nodeinfo['value']
        anode.set_attrs({'collapsed': False})
    if 'children' in nodeinfo.keys():
        for c in nodeinfo['children']:
            notused = import_tree_from_dict(c, parent=anode)
    return anode

def read_tree(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return import_tree_from_dict(data)

class Interaction:
    def __init__(self, root, ax, canvas, separations={'subtree': 0.5, 'level': 50, 'sibling': 0.1}):
        self.root = root 
        self.ax = ax
        self.canvas = canvas
        self.separations = separations
        self.clicked = None
        self.draw()
        
    def onclick(self, event):
        self.clicked = None
        q = np.array([event.xdata, event.ydata])
        _min = np.inf
        for node in iterators.postorder_iter(self.root):
            p = np.array([node.x, node.y])
            d = np.linalg.norm(p-q, ord=np.inf)
            if d < 1:
                self.clicked = node 
                break
        self.draw()

    def draw(self):
        self.ax.clear()
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_axis_off()
        reingold_tilford(self.root, 
                         sibling_separation=self.separations['sibling'], 
                         subtree_separation=self.separations['subtree'], 
                         level_separation=self.separations['level'])
        # turn vertical layout to horizontal layout
        for node in iterators.postorder_iter(self.root):
            node.x, node.y = -node.y, node.x
        plot_tree(self.root, ax=ax, color='black', markerfacecolor='red', markersize=10, marker='o')
        if self.clicked is not None:
            txt = ax.annotate(f'{self.clicked.name}: {self.clicked.value}', 
                        [self.clicked.x, self.clicked.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='left', verticalalignment='center',
                        xytext=(5, 0), textcoords='offset points')
            txt.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white'))
            
        self.canvas.draw()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize tree with node-link representation')
    parser.add_argument('-i', '--input', type=str, default='flare.json', help='Filename of tree dataset')
    args = parser.parse_args()

    root = read_tree(args.input)

    fig, ax = plt.subplots(1,1, figsize=(12, 8))

    inter = Interaction(root, ax=ax, canvas=fig.canvas)
            
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.set_aspect('equal') 
    plt.tight_layout()
    cid = fig.canvas.mpl_connect('button_press_event', inter.onclick)
    plt.show()
