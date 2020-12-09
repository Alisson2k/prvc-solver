class Cromossomo(object):
    def __init__(self, dna, aptidao_dist, aptidao_cars, qt_restricoes=0):
        self.dna = dna
        self.aptidao_dist = aptidao_dist
        self.aptidao_cars = aptidao_cars
        self.qt_restricoes = qt_restricoes

    def aumenta_restricao(self):
        self.qt_restricoes += 1

    def clone(self):
        return Cromossomo(self.dna, self.aptidao_dist, self.aptidao_cars, self.qt_restricoes)

    def __str__(self):
        return f'[dna: {self.dna}, aptidao_dist: {self.aptidao_dist}, aptidao_cars: {self.aptidao_cars}, qt_restricoes: {self.qt_restricoes}]'