from App.Views import CsvConfig as View


class CsvConfig:
    def __init__(self, result):
        self.result = result
        self.view = View.CsvConfig(self)
