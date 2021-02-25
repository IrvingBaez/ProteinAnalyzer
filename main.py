import math
from numpy import dot
from numpy.linalg import norm

total_proteins = ["B EA", "BEAe", "AXEBE", "XK"]


def iaf(domain):
    domain_proteins = [protein for protein in total_proteins if domain in protein]
    print(domain_proteins)
    return math.log(len(total_proteins) / len(domain_proteins), 2)


def iv(domain):
    distinct_domain = []

    for protein in [protein for protein in total_proteins if domain in protein]:
        # Find index(es) of domain
        indexes = [i for i, block in enumerate(protein) if block == domain]
        for index in indexes:
            if index + 1 < len(protein) and not protein[index + 1] == " " and not protein[index + 1] in distinct_domain:
                distinct_domain += [protein[index + 1]]
            if index - 1 >= 0 and not protein[index - 1] == " " and not protein[index - 1] in distinct_domain:
                distinct_domain += [protein[index - 1]]

    print(distinct_domain)
    return 1 / len(distinct_domain)


def weight_score(domain):
    return iaf(domain) * iv(domain)


def sim(x, y):
    return dot(x, y) / (norm(x) * norm(y))


def order(x, y):
    # I HAVE SEVERAL QUESTIONS
    # Qs y Qt?
    return None


if __name__ == '__main__':
    print(iaf("A"))
    print(iv("A"))
    print(weight_score("A"))
    print(weight_score("B"))
    # No as described in document.
