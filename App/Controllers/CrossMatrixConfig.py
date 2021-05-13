from App.Views import CrossMatrixConfig as View


class CrossMatrixConfig:
    def __init__(self, caller):
        self.caller = caller
        self.view = View.CrossMatrixConfig(self)
