from App.Views import CrossMatrixConfig as View


class CrossMatrixConfig:
    def __init__(self, data):
        self.data = data
        self.view = View.CrossMatrixConfig(self)
