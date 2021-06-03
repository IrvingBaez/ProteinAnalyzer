from tkinter import *
from tkinter import filedialog, ttk
from pubsub import pub

from App.Views.Views import display_error, set_scrollbars, dataframe_to_treeview


class MainView:
    def __init__(self, controller):
        pub.subscribe(display_error, "Error")
        self.controller = controller
        self.root = Tk()

        self.tabControl = ttk.Notebook(self.root)
        self.set_up_window()
        self.set_up_menu()

        self.root.mainloop()

    def set_up_window(self):
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.title("Protein Analyzer")
        self.root.option_add('*tearOff', False)

    def set_up_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        # File menu
        file_menu = Menu(menu)
        menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cargar", command=self.load_command)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit())

        # Analyze menu
        analyze_menu = Menu(menu)
        menu.add_cascade(label="Analizar", menu=analyze_menu)
        analyze_menu.add_command(label="Puntuación Ponderada", command=self.weighted_scores_command)

    def load_command(self):
        file_path = filedialog.askopenfilename(title="Seleccione un archivo", filetypes=(
            ("Archivos csv", "*.csv"), ("Archivos txt", "*.txt")
        ))
        self.controller.load_data(file_path)

        frame = LabelFrame(self.root, text="Datos")
        frame.place(relheight=1, relwidth=1)

        tree_view = ttk.Treeview(frame)
        tree_view.place(relheight=1, relwidth=1)

        set_scrollbars(tree_view)
        dataframe_to_treeview(self.controller.data, tree_view)

    def weighted_scores_command(self):
        self.controller.weighted_scores()
