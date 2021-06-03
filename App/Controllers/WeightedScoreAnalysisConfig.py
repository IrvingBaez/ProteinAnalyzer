from App.Views import WeightedScoreAnalysisConfig as View
from App.Controllers.WeightedScoreAnalysis import WeightedScoreAnalysis


class WeightedScoreAnalysisConfig:
    def __init__(self, data):
        self.data = data
        self.analyzer = None
        self.view = View.WeightedScoreAnalysisConfig(self)

    def perform_analysis(self, id_col, sequence_col, separator):
        self.analyzer = WeightedScoreAnalysis(self.data, id_col, sequence_col, separator)
