from tkinter import *
from tkinter import ttk, filedialog


class CrossMatrixConfig:
    def __init__(self, controller):
        self.include_nan = IntVar(value=1)
        self.controller = controller
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        # Contenedor de botones
        button_container = LabelFrame(popup, text="Opciones")
        button_container.pack(side=TOP, fill=X)

        self.inclide_nan_box = ttk.Checkbutton(button_container,
                                               text="Incluir datos sin puntuación",
                                               variable=self.include_nan,
                                               onvalue=1,
                                               offvalue=0)
        var = IntVar()
        radio1 = Radiobutton(button_container, text="Más altos", variable=var, value=1)
        radio2 = Radiobutton(button_container, text="Más bajos", variable=var, value=2)
        radio1.pack(anchor=W)
        radio2.pack(anchor=W)

        self.inclide_nan_box.pack()

        self.graph_button = ttk.Button(popup, text="Graficar", command=self.graph)
        self.graph_button.pack()

    def graph(self):
        save_dialog = filedialog.asksaveasfile(mode='a', defaultextension=".csv")

        if save_dialog is None:
            return

        if self.include_nan.get() == 0:
            filtered = self.controller.result[self.controller.result['Puntuación'].notna()]
            print(filtered)

            filtered.to_csv(save_dialog.name, index=False)
        else:
            self.controller.result.to_csv(save_dialog.name, index=False)
