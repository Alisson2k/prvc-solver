import math
import sys
import random

from population import Population
from ambiente import Ambiente
from cromossomo import Cromossomo
from functools import cmp_to_key
from utils import compare

# quantidade de iteracoes
iterations = 1

instance = './instances/'

# instância que será usada
filename = instance + 'P-n16-k8.txt'
veiculos = 4

f = open(filename, 'r')
lines = f.readlines()

ambiente = Ambiente()

# pega a dimensao e capacidade
dimension = lines[3].split(' : ')[1]
dimension = int(dimension[0:len(dimension) - 1])
capacidade = lines[5].split(' : ')[1]
capacidade = int(capacidade[0:len(capacidade) - 1])

pesos = [ 0 for i in range(dimension) ]
distancia = [ [ 0 for i in range(dimension) ] for j in range(dimension) ]
coord = [ [ 0 for i in range(2) ] for j in range(dimension) ]

l_index = 7
for i in range(dimension):
    line = lines[l_index][0:len(lines[l_index]) - 1]
    id = int(line.split(' ')[0]) - 1
    x = int(line.split(' ')[1])
    y = int(line.split(' ')[2])

    coord[id][0] = x
    coord[id][1] = y

    l_index += 1

l_index += 1
for i in range(dimension):
    line = lines[l_index][0:len(lines[l_index]) - 1]
    id = int(line.split(' ')[0]) - 1
    demand = int(line.split(' ')[1])

    pesos[id] = demand
    l_index += 1

for i in range(dimension):
    for j in range(dimension):
        distancia[i][j] = math.sqrt(((coord[i][0] - coord[j][0]) ** 2) + ((coord[i][1] - coord[j][1]) ** 2))
        distancia[j][i] = math.sqrt(((coord[i][0] - coord[j][0]) ** 2) + ((coord[i][1] - coord[j][1]) ** 2))

ambiente.pesos = pesos
ambiente.distancia_c = distancia
ambiente.capacidade_veiculos = capacidade
ambiente.quantidade_veiculos = veiculos

population = Population()
population.generate(ambiente)

def avalia_populacao(population, ambiente):
    for cromo in population:
        ambiente.arruma_cromo(cromo)
        ambiente.primeira_avaliacao(cromo)
        ambiente.segunda_avaliacao(cromo)

def elitismo(population, limit):
    nova_pop = []

    # ordena a população
    # na seguinte ordem crescente: [qt_restricoes, aptidao_dist, aptidao_cars]
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
    population.sort(key=c_sort)

    for i in range(limit):
        nova_pop.append(population[i].clone())

    return nova_pop

def selecao_roleta(population, limit):
    individuos = []
    sum = 0

    for cromo in population:
        sum += cromo.aptidao_dist / cromo.aptidao_cars

    for i in range(limit):
        aux = 0
        numero_aleatorio = random.randint(0, math.floor(sum))

        for j in range(len(population)):
            aux += population[j].aptidao_dist / population[j].aptidao_cars
            if j == 0:
                continue

            if aux > numero_aleatorio:
                pop = population[j - 1]
                individuos.append(Cromossomo(pop.dna, pop.aptidao_dist, pop.aptidao_cars, pop.qt_restricoes))
                break

    return individuos

def selecao_torneio(population, limit):
    individuos = []
    nova_pop = []

    for i in range(min(math.floor(limit * 1.5), len(population))):
        individuos.append(population[random.randint(0, len(population) - 1)].clone())

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
    population.sort(key=c_sort)

    for i in range(limit):
        nova_pop.append(individuos[i].clone())

    return nova_pop

# def selecao_torneio(population, limit):
#     individuos = []

#     for i in range(math.floor(len(population) / 3) + 2):
#         individuos.append(population[random.randint(0, len(population) - 1)].clone())

#     return individuos

def crossover_pmx(population):
    nova_pop = []

    for i in range(len(population)):
        for j in range(len(population)):
            if i == j:
                continue

            ponto_de_corte = random.randint(0, len(population[i].dna))
            new_dna = []

            for k in range(min(len(population[i].dna), len(population[j].dna))):
                if k <= ponto_de_corte:
                    new_dna.append(population[i].dna[k])
                else:
                    new_dna.append(population[j].dna[k])

            nova_pop.append(Cromossomo(new_dna, 0, 0))

    return population

def mutacao_aleatoria(population):
    if len(population) == 0:
        return

    qt_individuos = random.randint(0, len(population) - 1)

    for i in range(qt_individuos):
        qt_mutacoes = random.randint(0, math.floor(len(population[i].dna) / 3))
        for j in range(qt_mutacoes):
            posicao_1 = random.randint(0, len(population[i].dna) - 1)
            posicao_2 = random.randint(0, len(population[i].dna) - 1)

            aux_1 = population[i].dna[posicao_1]
            aux_2 = population[i].dna[posicao_2]

            population[i].dna[posicao_1] = aux_2
            population[i].dna[posicao_2] = aux_1

def mutacao_reversa(population):
    return population.reverse()

def resolve(population, max_gen, limit):
    result = 0
    menor_distancia = sys.float_info.max
    cont_max_distancia = 0

    for j in range(10):
        for k in range(iterations):
            for i in range(max_gen):
                avalia_populacao(population.population, ambiente)

                melhores_idvs = elitismo(population.population, math.ceil(limit * 0.1))

                seleciona_indv = selecao_torneio(population.population, limit)
                # seleciona_indv = selecao_roleta(population.population, limit)
                # seleciona_indv = selecao_roleta(population.population, limit)

                nova_populacao = crossover_pmx(seleciona_indv)

                avalia_populacao(nova_populacao, ambiente)

                # 5% de chance de mutacao
                if random.randint(0, 100) < 5:
                    mutacao_aleatoria(nova_populacao)
                if random.randint(0, 100) < 5:
                    mutacao_reversa(nova_populacao)

                avalia_populacao(nova_populacao, ambiente)

                population.population = []
                population.population.extend(nova_populacao)
                population.population.extend(melhores_idvs)

            if population.pega_menor().aptidao_dist == menor_distancia:
                if cont_max_distancia == 100:
                    break
                else:
                    cont_max_distancia = 0

        result += population.pega_menor().aptidao_dist

    print("Menor caminho: " + str(result / 10))

resolve(population, 10, 10)