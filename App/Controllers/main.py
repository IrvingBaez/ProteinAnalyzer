import pandas as pd
from pubsub import pub

from App.Controllers.WeightedScoreAnalysisConfig import WeightedScoreAnalysisConfig
from App.Views.main import MainView


class MainController:
    def __init__(self):
        self.data = None
        self.view = MainView(self)

    def load_data(self, path):
        try:
            self.data = pd.read_csv(path)
        except ValueError:
            pub.sendMessage("Error", message="Archivo no válido")
        except FileNotFoundError:
            pub.sendMessage("Error", message="Archivo no encontrado")

    def weighted_scores(self):
        WeightedScoreAnalysisConfig(self.data)


if __name__ == '__main__':
    MainController()
