from tkinter import *
from tkinter import ttk, filedialog


class CsvConfig:
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
        self.inclide_nan_box.pack()

        self.export_button = ttk.Button(popup, text="Exportar", command=self.export)
        self.export_button.pack()

    def export(self):
        save_dialog = filedialog.asksaveasfile(mode='a', defaultextension=".csv")

        if save_dialog is None:
            return

        if self.include_nan.get() == 0:
            filtered = self.controller.result[self.controller.result['Puntuación'].notna()]
            print(filtered)

            filtered.to_csv(save_dialog.name, index=False)
        else:
            self.controller.result.to_csv(save_dialog.name, index=False)
