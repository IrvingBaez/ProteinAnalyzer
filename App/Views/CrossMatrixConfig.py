from tkinter import *
from tkinter import ttk, filedialog

import numpy
from matplotlib import pyplot as plt

from App.Views.Views import set_scrollbars, dataframe_to_treeview


class CrossMatrixConfig:
    def __init__(self, controller):
        self.controller = controller
        self.neighbours = controller.data
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        # Button container
        button_container = LabelFrame(popup, text="Opciones")
        button_container.pack(side=TOP, fill=X)

        # Number of elements
        self.element_text = ttk.Entry(button_container, text="Número de elementos")
        self.element_text.pack(anchor=W)

        # High or low
        self.selection = IntVar(value=1)
        radio1 = Radiobutton(button_container, text="Más altos", variable=self.selection, value=1)
        radio2 = Radiobutton(button_container, text="Más bajos", variable=self.selection, value=2)
        radio1.pack(anchor=W)
        radio2.pack(anchor=W)

        self.graph_button = ttk.Button(popup, text="Graficar", command=self.plot)
        self.graph_button.pack()

    def plot(self):
        # Domains sorted by number of distinct neighbours
        neighbours_count = [[key, len(val)] for key, val in self.neighbours.items()]
        neighbours_count.sort(key=lambda x: x[1], reverse=self.selection.get() == 1)

        # Extracting relevant domain names
        limit = int(self.element_text.get())
        domains = list(map(lambda x: x[0], neighbours_count[0:limit]))

        # Creating matrix and counting relations
        matrix = numpy.zeros((len(domains), len(domains)))
        for domain in domains:
            for neighbour in self.neighbours[domain]:
                if neighbour in domains:
                    matrix[domains.index(domain)][domains.index(neighbour)] += 1

        fig, ax = plt.subplots()
        im = ax.imshow(matrix)

        # We want to show all ticks...
        ax.set_xticks(numpy.arange(len(domains)))
        ax.set_yticks(numpy.arange(len(domains)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(domains)
        ax.set_yticklabels(domains)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        for i in range(len(domains)):
            for j in range(len(domains)):
                text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")

        ax.set_title("Heatmap")
        fig.tight_layout()
        plt.show()
