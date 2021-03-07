import pandas as pd
from pubsub import pub


class MainController:
    def __init__(self):
        self.data = None

    def load_data(self, path):
        try:
            self.data = pd.read_csv(path)
        except ValueError:
            pub.sendMessage("Error", message="Archivo no válido")
        except FileNotFoundError:
            pub.sendMessage("Error", message="Archivo no encontrado")
