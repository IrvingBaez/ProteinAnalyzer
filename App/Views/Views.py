from tkinter import *
from tkinter import messagebox


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
    treeview.delete(*treeview.get_children())

    treeview["column"] = list(dataframe.columns)
    treeview["show"] = "headings"

    for column in treeview["columns"]:
        treeview.heading(column, text=column)  # let the column heading = column name

    rows = dataframe.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in rows:
        treeview.insert("", "end", values=row)  # inserts each list into the treeview.