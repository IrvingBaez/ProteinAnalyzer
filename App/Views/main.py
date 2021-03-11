from App.Controllers.main import *
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from pubsub import pub


def display_error(message="Algo salió mal"):
    messagebox.showerror("Information", message)


def set_scrollbars(tree_view, vertical=True, horizontal=False):
    if vertical:
        treescrolly = Scrollbar(tree_view, orient=VERTICAL, command=tree_view.yview)
        treescrolly.pack(side=RIGHT, fill=Y)
        tree_view.configure(yscrollcommand=treescrolly.set)
    if horizontal:
        treescrollx = Scrollbar(tree_view, orient=HORIZONTAL, command=tree_view.xview)
        treescrollx.pack(side=BOTTOM, fill=X)
        tree_view.configure(xscrollcommand=treescrollx.set)


def dataframe_to_treeview(dataframe, treeview):
    treeview["column"] = list(dataframe.columns)
    treeview["show"] = "headings"

    for column in treeview["columns"]:
        treeview.heading(column, text=column)  # let the column heading = column name

    rows = dataframe.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in rows:
        treeview.insert("", "end", values=row)  # inserts each list into the treeview.


class MainView:
    def __init__(self):
        pub.subscribe(display_error, "Error")
        self.main_controller = MainController()
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
        self.main_controller.load_data(file_path)

        frame = LabelFrame(self.root, text="Datos")
        frame.place(relheight=0.95, relwidth=0.9)

        tree_view = ttk.Treeview(frame)
        tree_view.place(relheight=1, relwidth=1)

        set_scrollbars(tree_view)
        dataframe_to_treeview(self.main_controller.data, tree_view)

    def weighted_scores_command(self):
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        frame = LabelFrame(popup, text="Datos")
        frame.place(relheight=0.95, relwidth=0.9)

        tree_view = ttk.Treeview(frame)
        tree_view.place(relheight=1, relwidth=1)

        set_scrollbars(tree_view)
        dataframe_to_treeview(self.main_controller.weighted_scores(), tree_view)


if __name__ == '__main__':
    MainView()
