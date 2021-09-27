from App.Models import WeightedScoreAnalysis as Model
from App.Views import WeightedScoreAnalysis as View
from App.Controllers.CsvConfig import CsvConfig
from App.Controllers.CrossMatrixConfig import CrossMatrixConfig


class WeightedScoreAnalysis:
    def __init__(self, data, type_col, id_col, sequence_col, separator):
        # self.data = data[[id_col, sequence_col]]
        self.model = Model.WeightedScoreAnalysis(data, type_col, id_col, sequence_col, separator)
        self.result = self.model.weighted_score_per_family_type()
        self.view = View.WeightedScoreAnalysis(self)

        self.crossMatrixConfig = None

    def show_heatmap(self):
        self.crossMatrixConfig = CrossMatrixConfig(self.model.neighbours)
        # self.model.cross_matrix()

    def save_as_csv(self):
        CsvConfig(self.result)

    def score_graph(self):
        self.model.score_graph()
