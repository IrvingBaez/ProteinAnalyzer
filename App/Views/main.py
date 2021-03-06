from App.Controllers.main import *
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from pubsub import pub


def display_error(message="Algo salió mal"):
    messagebox.showerror("Information", message)


class MainView:
    def __init__(self):
        pub.subscribe(display_error, "Error")
        self.main_controller = MainController()
        self.root = Tk()

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
        self.main_controller.load_data(file_path)

        data_frame = LabelFrame(self.root, text="Datos")
        data_frame.place(relheight=0.95, relwidth=0.9)
        tree_view = ttk.Treeview(data_frame)
        tree_view.place(relheight=1, relwidth=1)

        treescrolly = Scrollbar(data_frame, orient="vertical", command=tree_view.yview)
        treescrollx = Scrollbar(data_frame, orient="horizontal", command=tree_view.xview)
        tree_view.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        tree_view["column"] = list(self.main_controller.data.columns)
        tree_view["show"] = "headings"

        for column in tree_view["columns"]:
            tree_view.heading(column, text=column)  # let the column heading = column name

        rows = self.main_controller.data.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in rows:
            tree_view.insert("", "end", values=row)  # inserts each list into the treeview.

        # TODO: Show data as table

    def weighted_scores_command(self):
        pass


if __name__ == '__main__':
    MainView()
