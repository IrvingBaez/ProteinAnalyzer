from App.Models import WeightedScoreAnalysis as Model
from App.Views import WeightedScoreAnalysis as View


class WeightedScoreAnalysis:
    def __init__(self, data):
        self.data = data
        self.model = Model.WeightedScoreAnalysis()
        self.result = self.model.weight_score_per_family(data)
        self.view = View.WeightedScoreAnalysis(self)

    def show_heatmap(self):
        self.model.cross_matrix()
