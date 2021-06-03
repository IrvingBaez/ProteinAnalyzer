from tkinter import *
from tkinter import ttk, filedialog

from App.Views.Views import set_scrollbars, dataframe_to_treeview


class WeightedScoreAnalysis:
    def __init__(self, controller):
        self.controller = controller
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        # TreeView container
        frame = LabelFrame(popup, text="Datos")
        frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.tree_view = ttk.Treeview(frame)
        self.tree_view.pack(side=TOP, fill=BOTH, expand=True)

        set_scrollbars(self.tree_view)
        dataframe_to_treeview(self.controller.result, self.tree_view)

        # Buttons container
        button_container = LabelFrame(popup, text="Opciones")
        button_container.pack(side=RIGHT, fill=Y)
        
        self.sort_button = ttk.Button(button_container, text="Ordenar por Valor", command=self.sort_by_value)
        self.sort_button.pack(fill=X)

        save_button = ttk.Button(button_container, text="Exportar csv", command=self.controller.save_as_csv)
        save_button.pack(fill=X)

        heatmap_button = ttk.Button(button_container, text="Mapa de calor", command=self.controller.show_heatmap)
        heatmap_button.pack(fill=X)

        score_graph_button = ttk.Button(button_container, text="Graficar puntuaciones",
                                        command=self.controller.score_graph)
        score_graph_button.pack(fill=X)

    def sort_by_value(self):
        dataframe_to_treeview(self.controller.result.sort_values('Puntuación', ascending=False), self.tree_view)
        self.sort_button.configure(text="Ordenar por Dominio", command=self.sort_by_domain)

    def sort_by_domain(self):
        dataframe_to_treeview(self.controller.result.sort_values('Dominio', ascending=True), self.tree_view)
        self.sort_button.configure(text="Ordenar por Valor", command=self.sort_by_value)
