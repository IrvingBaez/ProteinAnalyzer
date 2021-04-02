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
    def __init__(self):
        self.total_proteins = None
        self.neighbours = {}
        self.result = None

    def weight_score_per_family(self, data):
        """
        Finds the weighted score for every family available in the data provided.

        :param data: pandas dataframe, table of proteins and their families.
        :return: pandas dataframe with domain and weighted score as columns.
        """
        self.__load_proteins(data)

        data = {'Dominio': [], 'Puntuación': [], 'Vecinos': []}
        for family in self.__find_families():
            data['Dominio'] += [family]
            data['Puntuación'] += [self.__weighted_score(family)]

            neighbours = self.neighbours.get(family)
            if neighbours is not None:
                data['Vecinos'] += [', '.join(neighbours.keys())]
            else:
                data['Vecinos'] += ['']

        self.result = pd.DataFrame(data, columns=['Dominio', 'Puntuación', 'Vecinos']).sort_values('Dominio')

        return self.result

    def cross_matrix(self):
        neighbours_count = [[key, len(val)] for key, val in self.neighbours.items()]
        neighbours_count.sort(key=lambda x: x[1], reverse=True)

        domains = list(map(lambda x: x[0], neighbours_count[0:10]))
        matrix = numpy.zeros((len(domains), len(domains)))

        for domain in domains:
            for neighbour in self.neighbours[domain]:
                if neighbour in domains:
                    matrix[domains.index(domain)][domains.index(neighbour)] += 1

        fig, ax = plt.subplots()
        im = ax.imshow(matrix)

        # We want to show all ticks...
        ax.set_xticks(numpy.arange(len(domains)))
        ax.set_yticks(numpy.arange(len(domains)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(domains)
        ax.set_yticklabels(domains)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        for i in range(len(domains)):
            for j in range(len(domains)):
                text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")

        ax.set_title("Heatmap")
        fig.tight_layout()
        plt.show()

    def __load_proteins(self, data):
        """
        Saves data into a dict where ID is the key and HMMER is the value as a list of strings,
        each representing a domain.

        :param data: pandas dataframe, table of proteins and their families.
        :return: None.
        """
        data['HMMER'] = data.HMMER.str.replace(r'\([^()]*\)', '', regex=True)
        self.total_proteins = {key: [domain for domain in value.split('+')]
                               for key, value in data.set_index('ID').T.to_dict('records')[0].items()}

    def __weighted_score(self, domain):
        """
        Weighted score is defined as IAV(d) * IV(d) where:
            d is a domain
            IAV is inverse abundance frequency function
            IV is inverse variability function

        :param domain: string, domain d.
        :return: positive number or nan if domain never has any neighbours.
        """
        return self.__inverse_abundance_frequency(domain) * self.__inverse_variability(domain)

    def __inverse_abundance_frequency(self, domain):
        """
        Defined as log(pt/pd) where pt is the number of total proteins and pd is the number of proteins containing
        domain d.

        :param domain: string, domain d.
        :return: number equal or greater than 1.
        """
        domain_proteins = [protein for protein in self.total_proteins.values() if domain in protein]
        return math.log(len(self.total_proteins) / len(domain_proteins), 10)

    def __inverse_variability(self, domain):
        """
        Is defined as 1 / the number of different domain families adjacent to a domain.

        :param domain: string, domain to process.
        :return: a number between 1 and 0 or nan if the domain never has any neighbours.
        """
        distinct_neigbours = len(self.__distinct_neighbours(domain))
        return 1 / distinct_neigbours if 0 < distinct_neigbours else numpy.nan

    def __distinct_neighbours(self, domain):
        """
        Finds all naighbours of domain d without repetition.

        :param domain: domain d.
        :return: list of neighbours.
        """
        neighbours = []
        for protein in [protein for protein in self.total_proteins.values() if domain in protein]:
            neighbour_indexes = [[index - 1, index + 1] for index, value in enumerate(protein) if value == domain]
            neighbours += [protein[i] for i in sum(neighbour_indexes, []) if i in range(0, len(protein))]

        self.__register_neighbours(domain, neighbours)
        return list(set(neighbours))

    def __register_neighbours(self, domain, neighbours):
        if len(neighbours) > 0:
            self.neighbours[domain] = {}

        for neighbour in neighbours:
            if neighbour not in self.neighbours[domain]:
                self.neighbours[domain][neighbour] = 1
            else:
                self.neighbours[domain][neighbour] += 1

    def __find_families(self):
        """
        Finds all distinct families in self.total_proteins.

        :return: set of families.
        """
        return set(sum(self.total_proteins.values(), []))
