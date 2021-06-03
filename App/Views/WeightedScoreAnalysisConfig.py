from tkinter import *
from tkinter import ttk, filedialog


class WeightedScoreAnalysisConfig:
    def __init__(self, controller):
        self.include_nan = IntVar(value=1)
        self.controller = controller
        popup = Toplevel()
        popup.geometry("500x500+0+0")
        popup.grab_set()

        # Container
        button_container = LabelFrame(popup, text="Opciones")
        button_container.pack(side=TOP, fill=X)

        # Labels
        Label(button_container, text="Columna de ID:").grid(pady=5, row=0, column=0)
        Label(button_container, text="Columna de secuencia:").grid(pady=5, row=1, column=0)
        Label(button_container, text="Separador:").grid(pady=5, row=2, column=0)

        # Select for id column
        self.id_combo = ttk.Combobox(button_container, state="readonly")
        self.id_combo["values"] = self.controller.data.columns.tolist()
        self.id_combo.current(0)
        self.id_combo.grid(pady=5, row=0, column=1)

        # Select for sequence column
        self.seq_combo = ttk.Combobox(button_container, state="readonly")
        self.seq_combo["values"] = self.controller.data.columns.tolist()
        self.seq_combo.current(0)
        self.seq_combo.grid(pady=5, row=1, column=1)

        # Input for separator
        self.sep_text = ttk.Entry(button_container)
        self.sep_text.grid(pady=5, row=2, column=1)

        # Submit button
        self.submit = ttk.Button(button_container, text="Aceptar", command=self.submit)
        self.submit.grid(pady=5, row=3, column=1, columnspan=2)

    def submit(self):
        self.controller.perform_analysis(self.id_combo.get(), self.seq_combo.get(), self.sep_text.get())
