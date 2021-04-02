from tkinter import *
from tkinter import ttk, filedialog
import csv

from App.Views.Views import set_scrollbars, dataframe_to_treeview


class WeightedScoreAnalysis:
    def __init__(self, controller):
        self.controller = controller
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        # Contenedor de treeview
        frame = LabelFrame(popup, text="Datos")
        frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.tree_view = ttk.Treeview(frame)
        self.tree_view.pack(side=TOP, fill=BOTH, expand=True)

        set_scrollbars(self.tree_view)
        dataframe_to_treeview(self.controller.result, self.tree_view)

        # Contenedor de botones
        buttons = LabelFrame(popup, text="Opciones")
        buttons.pack(side=RIGHT, fill=Y)
        
        self.sort_button = ttk.Button(buttons, text="Ordenar por Valor", command=self.sort_by_value)
        self.sort_button.pack()

        save_button = ttk.Button(buttons, text="Exportar csv", command=self.save_as_csv)
        save_button.pack(fill=X)

        heatmap_button = ttk.Button(buttons, text="Mapa de calor", command=self.show_heatmap)
        heatmap_button.pack(fill=X)

    def sort_by_value(self):
        dataframe_to_treeview(self.controller.result.sort_values('Puntuación', ascending=False), self.tree_view)
        self.sort_button.configure(text="Ordenar por Dominio", command=self.sort_by_domain)

    def sort_by_domain(self):
        dataframe_to_treeview(self.controller.result.sort_values('Dominio', ascending=True), self.tree_view)
        self.sort_button.configure(text="Ordenar por Valor", command=self.sort_by_value)

    def save_as_csv(self):
        save_dialog = filedialog.asksaveasfile(mode='a', defaultextension=".csv")

        if save_dialog is None:
            return

        self.controller.result.to_csv(save_dialog.name, index=False)

    def show_heatmap(self):
        self.controller.show_heatmap()
