import csv
import math
import numpy

total_proteins = {}


def find_families():
    return set(sum(total_proteins.values(), []))


def iaf(domain):
    domain_proteins = [protein for protein in total_proteins.values() if domain in protein]

    return math.log(len(total_proteins) / len(domain_proteins), 10)


def iv(domain):
    distinct_neighbours = []
    for protein in [protein for protein in total_proteins.values() if domain in protein]:
        neighbour_indexes = [[index - 1, index + 1] for index, value in enumerate(protein) if value == domain]
        distinct_neighbours += [protein[i] for i in sum(neighbour_indexes, []) if i in range(0, len(protein))]

    # What to do when a domain appears only one without neighbours? len(set(distinct_neighbours)) == 0
    return 1 / len(set(distinct_neighbours))


def weight_score(domain):
    return iaf(domain) * iv(domain)


def weight_score_per_family():
    return {family: weight_score(family) for family in find_families()}


'''
Coefficient Variation was determined as the ratio of the standard deviation to the mean for all the Weighted Scores 
in the corresponding Transcription Factor family
'''


def coefficient_variation(data):
    return numpy.std(data, ddof=1) / numpy.mean(data)