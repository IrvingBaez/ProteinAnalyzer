import unittest
import pandas
import App.Models.WeightedScoreAnalysis as wsa


class WeightedScoreAnalysis(unittest.TestCase):
    def test_weight_score_per_family(self):
        analysis = wsa.WeightedScoreAnalysis()
        data = pandas.DataFrame(data={'ID': [1, 2, 3, 4], 'HMMER': ['a+b', 'c+a+b', 'a+b+x', 'a']})
        self.assertEqual(analysis.weight_score_per_family(data), {
            'x': 0.6020599913279623,
            'a': 0.0,
            'c': 0.6020599913279623,
            'b': 0.06246936830414995
        })


if __name__ == '__main__':
    unittest.main()
