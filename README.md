# CVRP SOLVER

The Capacitated Vehicle Routing Problem attempts to design better routes from a warehouse to a set of destinations, where each has specific restrictions, such as vehicle limitations, cost controls, time windows, resource limitations on loading at the warehouse, etc.

## Dataset

A public dataset was used to get test cases, here only three instances were saved, which is found in the `instances` folder. For more information about the dataset, all were extracted from [here](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

## Article Solution

The solution was expired in the article by the authors `Jadson José Monteiro Oliveira`, `Bruno Ramon de Almeida e Silva`, `Junior Marcos Bandeira`, which can be found [at](https://www.unibalsas.edu.br/wp-content/uploads/2017/01/ARTIGO-JADSON-OLIVEIRA.pdf), where they use a genetic algorithm to solve the problem. In this article, the authors implemented solutions in Java, but in this repository I opted for the Python because I believe it is closer to solutions like AI & ML.

That was the model they presented for the solution of this problem:

![UML](https://github.com/Alisson2k/prvc-solver/raw/master/common/images/UML.png)

### Classes

- **Ambiente**: represents the environment in which the population will be inserted.
- **Cromossomo**: represents the individuals in the solution.
- **Populacao**: represents the population itself.
- **AlgoritmoGenetico**: is composed of the methods corresponding to the processes imposed by the approach of a Genetic Algorithm

### Chromosomes

#### Selection

#### Mutation

### Decoding Solution

### Results obtained

## Instructions

As the project does not use any external library and does not need to install anythingn newin pip, there is not so much need to use a virtualenv, but it is up to you, however, it is mandatory to use **python3.6** or higher.

Tendo isso em mente basta executar 

```
python start.py
```

## Next steps

As the project was in a hurry at the time, not all of the code is in good condition, and my plan is to fix it in the future, in addition to better documenting the topics that were left above.

Some plans will also be to add test cases and graphs presenting results obtained, and facilitate the passing of parameters at the very time of executing the code.
