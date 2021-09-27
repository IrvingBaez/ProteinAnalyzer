from tkinter import *
from tkinter import ttk, filedialog

from App.Views.Views import set_scrollbars, dataframe_to_treeview


class WeightedScoreAnalysis:
    def __init__(self, controller):
        self.controller = controller
        self.tree_views = {}
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        self.tab_parent = ttk.Notebook(popup)
        for family_type in self.controller.result.keys():
            tab = ttk.Frame(self.tab_parent)
            self.tab_parent.add(tab, text=family_type)

            # TreeView container
            frame = LabelFrame(tab, text="Datos")
            frame.pack(side=LEFT, fill=BOTH, expand=True)

            tree_view = ttk.Treeview(frame)
            self.tree_views[family_type] = tree_view
            tree_view.pack(side=TOP, fill=BOTH, expand=True)

            set_scrollbars(tree_view)
            dataframe_to_treeview(self.controller.result[family_type], tree_view)

        # Buttons container
        button_container = LabelFrame(popup, text="Opciones")
        button_container.pack(side=RIGHT, fill=Y)

        self.sort_button = ttk.Button(button_container, text="Ordenar por Valor", command=self.sort_by_value)
        self.sort_button.pack(fill=X)

        save_button = ttk.Button(button_container, text="Exportar csv", command=self.controller.save_as_csv)
        save_button.pack(fill=X)

        heatmap_button = ttk.Button(button_container, text="Mapa de calor", command=self.controller.show_heatmap)
        heatmap_button.pack(fill=X)

        score_graph_button = ttk.Button(button_container, text="Graficar puntuaciones", command=self.cross_matrix_graph)
        score_graph_button.pack(fill=X)

        self.tab_parent.pack(expand=1, fill="both")

    def sort_by_value(self):
        family_type = self.tab_parent.tab(self.tab_parent.select(), "text")
        tree_view = self.tree_views[family_type]
        dataframe_to_treeview(self.controller.result[family_type].sort_values('Puntuación', ascending=False), tree_view)
        self.sort_button.configure(text="Ordenar por Dominio", command=self.sort_by_domain)

    def sort_by_domain(self):
        family_type = self.tab_parent.tab(self.tab_parent.select(), "text")
        tree_view = self.tree_views[family_type]
        dataframe_to_treeview(self.controller.result[family_type].sort_values('Dominio', ascending=True), tree_view)
        self.sort_button.configure(text="Ordenar por Valor", command=self.sort_by_value)

    def cross_matrix_graph(self):
        family_type = self.tab_parent.tab(self.tab_parent.select(), "text")
        self.controller.score_grap()