from typing import Dict,List,Tuple

from matplotlib import pyplot as mp1
import random

class KnapSackEvolver:
    def __init__(self, 
            items : Dict,                                   # values that define that evolutionary system
            itemRange : Tuple[int,int], 
            capacity : int,                                 # for knapsack 
            popSize: int, 
            iterations : int,                               # in irl you stop when things stop getting better 
            mutationRate : int,                             # mutation likelihood 
            crossOver : int):                               # mutation crosshover

        self._iterations : int = iterations                 # system max iterations
        self._populationSize : int = size
        self._geneLength - len(items.keys())                # gene or chromozone length (could be variables
        self._items = items
        
        print(self._items)

        self._geneMap = [self._items[k] for k in items.keys()]
        print(self._geneMap)

        self._itemRange = itemRange
        self._capicity = capacity
        self._crossover = crossOver # cross over chance
        self._mutationRate = mutationRate

        self._population = self.initializePopulation()


    # candidate solution
    # lengths of what kind of things
    # there are as many as there are gene lengths
    def spawnSolution(self) -> List[int]:
        (lower, upper) = self._itemRange
        return [random.randint(lower,upper) for _ int range(self._geneLength)]


    # get a list of candidates within our population
    def initializePopulation(self) -> List[List[int]]:
        return [self.spawnSolution() for _ in range(self._populationSize)]

    # work out how good the solution
    # get all weights for all items in the bag and sum them
    # as well check the utility value and good use case (of items in the bag)
    # utility_value = sum of all utility values
    # cost = sum of all weights
    # if a capaicity is greater than weight of the bag then discard the candidate/solution
    # final fitness = cost - utility_value (meaning there can be negative values)
    def fitness(self, gene : List[int]) -> int:
                        # weight       * number of items
        weights = [self._geneMap[i][0] * gene[i] for i in range(len(gene))]
        utilities = [self._geneMap[i][1] * gene[i] for i in range(len(gene))]

        cost = sum(weights)
        benefit = sum(utilities)

        if cost > self.capaicity:
            benefit = 0
            
        return benefit - cost

    def crossover(self, gene1 : List[int], gene2 : List[int]) -> List[int]:
        point = random.randint(0, len(gene1))
        child = []

        for i in range(len(gene1)):
            if i < point:
                child.append(gene1[i])
            else:
                child.append(gene2[i])

        return child

    def mutate(self, gene : List[int]) -> None:
        point = random.randint(0, len(gene))
        (lower, upper) = self._itemRange
        gene[point] = random.randint(lower, upper)

    def averageFitness(self, scored : List[Tuple]) -> float:
        total = 0
        for s in scored:
            total += s[0] 

        return total / len(scored)

    def visualize(self, performance : Tuple) -> None:
        xs = []
        ys = []
        
        for p in performance:
            xs.append(p[0])
            ys.append(p[1])

        mpl.xlabel('iterations')    
        mpl.ylabel('average fitness')


    def __repr__(self) -> str:
        gene = "\n"
        for g in self._population:
            x = self._fitness(g)
            gene += f"{g} : {x}"
        return gene


