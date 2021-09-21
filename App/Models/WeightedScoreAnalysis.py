import math
import numpy
import pandas as pd
import matplotlib.pyplot as plt


def coefficient_variation(data):
    """
    Coefficient Variation was determined as the ratio of the standard deviation to the mean for all the Weighted Scores
    in the corresponding Transcription Factor (CAZI) family

    :param data: should be a list of numbers
    :return: coefficient variation of the data
    """
    return numpy.std(data, ddof=1) / numpy.mean(data)


class WeightedScoreAnalysis:
    def __init__(self, data, type_col, id_col, sequence_col, separator):
        self.data = data[[type_col, id_col, sequence_col]]
        self.type_col = type_col
        self.id_col = id_col
        self.sequence_col = sequence_col
        self.separator = separator
        self.total_proteins = {}
        self.neighbours = {}
        self.result = None

        self.data[type_col] = self.data[type_col].str.strip()
        self.data[id_col] = self.data[id_col].str.strip()
        self.data[sequence_col] = self.data[sequence_col].str.strip()

    def weighted_score_per_family_type(self):
        self.__load_proteins(self.data)
        result = {}

        for family_type in self.total_proteins.keys():
            result[family_type] = self.__weight_score_per_family(family_type)

        return result

    def __weight_score_per_family(self, family_type):
        """
        Finds the weighted score for every family available in the data provided.

        :return: pandas dataframe with domain and weighted score as columns.
        """
        data = {'Dominio': [], 'Puntuación': [], 'Vecinos': []}
        for family in self.__find_families(family_type):
            data['Dominio'] += [family]
            data['Puntuación'] += [self.__weighted_score(family_type, family)]

            neighbours = self.neighbours[family_type].get(family)
            if neighbours is not None:
                data['Vecinos'] += [', '.join([f'{key} ({value})' for key, value in neighbours.items()])]
            else:
                data['Vecinos'] += ['']

        self.result = pd.DataFrame(data, columns=['Dominio', 'Puntuación', 'Vecinos']).sort_values('Dominio')

        return self.result

    def score_graph(self):
        """
        Plots the distribution of scores in a boxplot

        :return: None
        """
        scores = self.result['Puntuación'].tolist()
        scores = [score for score in scores if str(score) != 'nan']
        plt.boxplot(scores)
        plt.show()

    def __load_proteins(self, data):
        """
        Saves data into a dict where ID is the key and HMMER is the value as a list of strings,
        each representing a domain.

        :param data: pandas dataframe, table of proteins and their families.
        :return: None.
        """
        data[self.sequence_col] = data[self.sequence_col].str.replace(r'\([^()]*\)', '', regex=True)

        for family_type in data[self.type_col].unique():
            sub_data = data[data[self.type_col] == family_type]
            self.total_proteins[family_type] = {key: [domain for domain in value.split(self.separator)]
                                                for key, value in sub_data.set_index(self.id_col).T.to_dict('records')[1].items()}

    def __weighted_score(self, family_type, domain):
        """
        Weighted score is defined as IAV(d) * IV(d) where:
            d is a domain
            IAV is inverse abundance frequency function
            IV is inverse variability function

        :param domain: string, domain d.
        :return: positive number or nan if domain never has any neighbours.
        """
        return self.__inverse_abundance_frequency(family_type, domain) * self.__inverse_variability(family_type, domain)

    def __inverse_abundance_frequency(self, family_type, domain):
        """
        Defined as log(pt/pd) where pt is the number of total proteins and pd is the number of proteins containing
        domain d.

        :param domain: string, domain d.
        :return: number equal or greater than 1.
        """
        domain_proteins = [protein for protein in self.total_proteins[family_type].values() if domain in protein]
        return math.log(len(self.total_proteins[family_type]) / len(domain_proteins), 10)

    def __inverse_variability(self, family_type, domain):
        """
        Is defined as 1 / the number of different domain families adjacent to a domain.

        :param domain: string, domain to process.
        :return: a number between 1 and 0 or nan if the domain never has any neighbours.
        """
        distinct_neigbours = len(self.__distinct_neighbours(family_type, domain))
        return 1 / distinct_neigbours if 0 < distinct_neigbours else numpy.nan

    def __distinct_neighbours(self, family_type, domain):
        """
        Finds all naighbours of domain d without repetition.

        :param domain: domain d.
        :return: list of neighbours.
        """
        neighbours = []
        for protein in [protein for protein in self.total_proteins[family_type].values() if domain in protein]:
            neighbour_indexes = [[index - 1, index + 1] for index, value in enumerate(protein) if value == domain]
            neighbours += [protein[i] for i in sum(neighbour_indexes, []) if i in range(0, len(protein))]

        self.__register_neighbours(family_type, domain, neighbours)
        return list(set(neighbours))

    def __register_neighbours(self, family_type, domain, neighbours):
        self.neighbours[family_type] = {}

        if len(neighbours) > 0:
            self.neighbours[family_type][domain] = {}

        for neighbour in neighbours:
            if neighbour not in self.neighbours[family_type][domain]:
                self.neighbours[family_type][domain][neighbour] = 1
            else:
                self.neighbours[family_type][domain][neighbour] += 1

    def __find_families(self, family_type):
        """
        Finds all distinct families in self.total_proteins.

        :return: set of families.
        """
        return set(sum(self.total_proteins[family_type].values(), []))
