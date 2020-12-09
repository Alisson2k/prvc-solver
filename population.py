import random

from cromossomo import Cromossomo
from functools import cmp_to_key
from utils import compare

class Population(object):

    def __init__(self):
        self.limit = 10
        self.population = []

    def generate(self, ambiente):
        tamanho = len(ambiente.pesos)

        for i in range(self.limit):
            # gera um array de 1 a N de forma aleatoria, onde o primeiro e o ultimo elemento são 0's
            new_dna = list(range(1, tamanho))
            random.shuffle(new_dna)
            new_dna.insert(0, 0)
            new_dna.insert(len(new_dna), 0)

            self.population.append(Cromossomo(new_dna, 0, 0))

    def pega_menor(self):
        def custom_sort(c1, c2):
            compare_qt_restricoes = compare(c1.qt_restricoes, c2.qt_restricoes)
            compare_aptidao_dist = compare(c1.aptidao_dist, c2.aptidao_dist)
            compare_aptidao_cars = compare(c1.aptidao_cars, c2.aptidao_cars)

            if compare_qt_restricoes == 0:
                if compare_aptidao_dist == 0:
                    return compare_aptidao_cars
                else:
                    return compare_aptidao_dist
            else:
                return compare_qt_restricoes

        c_sort = cmp_to_key(custom_sort)
        self.population.sort(key=c_sort)

        return self.population[0]
