import pandas as pd
from pubsub import pub

from App.Models import WeightedScoreAnalysis as wsa


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

    def weighted_scores(self):
        analysis = wsa.WeightedScoreAnalysis()
        result = analysis.weight_score_per_family(self.data[["ID", "HMMER"]])
         # analysis.cross_matrix()
        return result
