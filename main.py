from typing import Dict,List,Tuple

from matplotlib import pyplot as mpl
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
        self._populationSize : int = popSize
        self._geneLength = len(items.keys())                # gene or chromozone length (could be variables
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
        return [random.randint(lower,upper) for _ in range(self._geneLength)]


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

        if cost > self._capicity:
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
        point = random.randint(0, len(gene)-1)
        (lower, upper) = self._itemRange
        x = random.randint(lower, upper)
        gene[point] = x

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
        mpl.plot(xs, ys)
        mpl.show()

    # toString
    # __str__ also works
    def __repr__(self) -> str:
        gene = "\n"
        for g in self._population:
            x = self.fitness(g)
            gene += f"{g} : {x}\n"
        return gene

    # children can replace parents in the next generation
    # you can be biased or lenient when you decide who survives to the next generation
    # (we are choosing the elitist route)
    def evolve(self) -> None:
        plotter = []

        for i in range(self._iterations):
            scored = [(self.fitness(self._population[p]), p) for p in range(self._populationSize)]     # calculate fitness of everyone
            scored.sort(key=lambda x: x[0], reverse=True)                                       # reverse so best are at the head
            plotter.append((i, self.averageFitness(scored)))

            cutoff = int(len(scored) * 0.8)  # 80 percent preservation
            for h in range(1,cutoff):
                roll = random.randint(0,99)
                if roll < self._crossover:
                    # breed with someone better
                    mate = scored[random.randint(0, h)][1]
                    fitParent = scored[h][0]
                    mate = scored[h][1]
                    child = self.crossover(self._population[mate], self._population[mate])
                    fitChild = self.fitness(child)

                    if fitChild > fitParent:
                        self.population[mate] = child


            for v in range(cutoff, len(scored)):
                iVictim = scored[v][1]
                self._population[iVictim] = self.spawnSolution()

            for m in range(1, len(scored)):
                roll = random.randint(0,99)
                if roll < self._mutationRate:
                    iMutation = scored[m][1]
                    self.mutate(self._population[iMutation])


        self.visualize(plotter)





items = {"food": (5,10), "water": (2, 20), "tent": (20,3), "medicine": (5,7), "clothes": (15,10)}
itemRange = (0,5)
capacity  = 50
popSize = 20
iter=100
mutaterate = 5
crossover = 20 

evo = KnapSackEvolver(items, itemRange, capacity, popSize, iter, mutaterate, crossover)
print(evo)
evo.evolve()
print(evo)
