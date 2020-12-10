import sys
import copy
from cromossomo import Cromossomo

class Ambiente(object):
    def __init__(self):
        self.taxa_mutacao = None
        self.taxa_elitismo = None
        self.capacidade_veiculos = None
        self.quantidade_veiculos = None
        self.distancia_c = None
        self.pesos = None # obj["pesos"]    

    """
    Quebra o dna dos cromossomos adicionando os 0's no meio dele
    baseado nos pesos e na capacidade de veiculos
    """
    def arruma_cromo(self, cromo: Cromossomo):
        cromo.aptidao_dist = 0
        cromo.aptidao_cars = 0
        cromo.qt_restricoes = 0

        container = [[]]

        j = 0
        sum = 0
        for i in range(len(cromo.dna)):
            sum += self.pesos[cromo.dna[i]]

            if sum > self.capacidade_veiculos:
                j += 1
                container.append([])
                sum = self.pesos[cromo.dna[i]]
            elif cromo.dna[i] == 0:
                if i > 0:
                    if cromo.dna[i - 1] != 0:
                        j += 1
                        container.append([])
                else:
                    container.append([])
                    sum = self.pesos[0]

            if cromo.dna[i] != 0:
                container[j].append(cromo.dna[i])

        new_dna = []
        aux_qt = copy.deepcopy(self.quantidade_veiculos)

        for i in range(len(container)):
            for j in range(len(container[i])):
                new_dna.append(container[i][j])

            if len(new_dna) > 1:
                if new_dna[len(new_dna) - 1] != 0 and aux_qt > 1:
                    new_dna.append(0)
                    aux_qt -= 1
                elif new_dna[len(new_dna) - 1] != 0:
                    new_dna.append(0)
                    cromo.aumenta_restricao()
            else:
                new_dna.append(0)

        cromo.dna = new_dna
        cromo_set = set()
        for i in range(len(cromo.dna)):
            if cromo.dna[i] in cromo_set and cromo.dna[i] != 0:
                cromo.dna.remove(i)
                continue

            cromo_set.add(cromo.dna[i])

        sum = 0

        for i in range(len(self.pesos)):
            if i not in cromo_set:
                sum += self.pesos[i]
                if sum > self.capacidade_veiculos:
                    cromo.dna.append(0)
                    sum = self.pesos[i]
                cromo.dna.append(i)

        if cromo.dna[0] != 0:
            cromo.dna.insert(0, 0)
        if cromo.dna[len(cromo.dna) - 1] != 0:
            cromo.dna.append(0)

    def primeira_avaliacao(self, cromo: Cromossomo):
        distancia = 0

        for i in range(len(cromo.dna) - 1):
            atual = cromo.dna[i + 1]
            anterior = cromo.dna[i]

            distancia += self.distancia_c[anterior][atual] # TODO: checar

        cromo.aptidao_dist = distancia

    def segunda_avaliacao(self, cromo: Cromossomo):
        contador = 0
        for c in cromo.dna:
            if c == 0:
                contador += 1

        cromo.aptidao_cars = contador