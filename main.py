# jmr cse 231 sec 001 honors project 11
''' Algorithm:
- Three main classes:
    1.  GA() maintains the population of individuals and simulates their
        interactions.
    2.  Individual() represents a single individual and an instance of its
        environment.
    3.  World() is imported and represents the environmental simulation for
        a single individual.
- During the simulation, for each generation:
    1.  Create the offspring by choosing fit parents and crossing their genes
    2.  Mutate the offspring at user-determined rates
    3.  Add the offspring to the main population
    4.  Kill off the weakest members of the population
    5.  Output the strongest member of the population'''

import random as rnd
import copy
import world

class Individual():
    def __init__(self, worldname="world1.txt"):
        "Create an individual with random traits in a certain world file."
        self.traits = [rnd.randint(-5,5) for i in range(6)]
        self.worldname = worldname
        self.env = world.World(worldname)
        self.fitnessRecent = False
    def __cmp__(self,other):
        "Compare this individual to another by fitness."
        return cmp(self.fitness, other.fitness)
    def __repr__(self):
        "Represent this individual."
        return self.__str__()
    def __str__(self):
        "Return this individual's genes as a string"
        return "Individual(" + str(self.traits) + ")"
    def mutate(self, mutation_rate):
        '''Mutate an individual by a certain rate and
        return a mutated individual.'''
        newindiv = copy.deepcopy(self)
        for i in range(6):
            if mutation_rate >= rnd.random():
                newindiv.traits[i] = rnd.randint(-5,5)
        newindiv.fitnessRecent = False
        return newindiv
    def crossover(self, other):
        '''Perform two-point crossover with this individual and another,
        returning two offspring individuals.'''
        point1 = rnd.randint(0,5)
        point2 = point1
        while point2 == point1:
            point2 = rnd.randint(0,5)
        if point2 < point1 :
            point1,point2 = point2,point1
        offspring1 = copy.deepcopy(self)
        offspring2 = copy.deepcopy(other)
        offspring1.traits[point1:point2],offspring2.traits[point1:point2] =\
        other.traits[point1:point2],self.traits[point1:point2]
        offspring1.fitnessRecent = False
        offspring2.fitnessRecent = False
        return offspring1, offspring2
    def getActuators (self):
        ''' Computes the values of the actuators (wheels) using the evolved matrix
        and the robot sensor values. Returns the value for the left wheel and the
        right wheel. '''
        matrix = self.traits
        sVals = self.env.getSensorValues()[0]
        leftWheel = 0
        rightWheel = 0
        acts = [0,0] 
      
        for i in range(0,2):
            for j in range(0, len(sVals)):
                matrixElem = i * len(sVals) + j
                acts[i] += matrix[matrixElem] * sVals[j]
                
        leftWheel = acts[0]
        rightWheel = acts[1]
        return leftWheel, rightWheel
    def evalfitness(self, moves=25):
        '''Run the robot through a new instance of the world to
        find out its fitness, return number of points'''
        score = 0
        self.env = world.World(self.worldname)
        for i in range(moves):
        # 1. Get sensor values from world
##            sensorValues, sensed = self.env.getSensorValues()
        # 2. Determine action
            lWheel, rWheel = self.getActuators()
        # 3. Move the robot
            if lWheel > 0 and rWheel > 0:
                self.env.moveAgent(1)
            if lWheel > 0 and not rWheel > 0:
                self.env.moveAgent(2)
            if not lWheel > 0 and rWheel > 0:
                self.env.moveAgent(0)
        # 4. Get the result
            if self.env.isBreadcrumb():
                score += 5
            if self.env.isDash():
                score += 1
            if self.env.isFinal():
                score += 10
        return score
    def getfitness(self):
        "If fitness is up to date and stored, return it. Otherwise, calculate it."
        if self.fitnessRecent:
            return self.__fitness
        else:
            self.__fitness = self.evalfitness()
            self.fitnessRecent = True
            return self.__fitness
    fitness = property(fget=getfitness)
class GA():
    def __init__(self,popSize=200,offspringPopSize=50,mutOffspring=50,\
                 mutBit=25,indivWorld="world1.txt"):
        '''Create a new GA population simulation. popSize=Size of population,
        offspringPopSize=Size of offspring population,mutOffspring=Percent
        of offspring to mutate,mutBit=Percent of genes to mutate during
        mutation,indivWorld=Name of txt file that contains world data.'''
        print ("Initializing Genetic Algorithm...",)
        self.population = [Individual(indivWorld) for i in range(popSize)]
        self.__popSize = popSize
        self.__offspringPopSize = offspringPopSize
        self.__mutOffspring = float(mutOffspring) / 100.0
        self.__mutBit = float(mutBit) / 100.0
        print ("Done!")
    def tournamentSelection(self,n,k):
        "Return the n best individuals from a random sample of size k"
        selection = rnd.sample(self.population, k)
        selection.sort()
        return selection[:n]
    def fitnessProportionateSelection(self, idx=False):
        '''Returns one individual using its fitness out of the total fitness
        as the probability of its selection from the population. If idx
        is true, return only the index of the selected individual in the
        population list.'''
        fitnessSum = sum([indiv.fitness for indiv in self.population])
        if fitnessSum: # If fitnessSum is nonzero
            randomValue = rnd.randint(1,fitnessSum)
            sumFitness = 0
            for num, indiv in enumerate(self.population):
                sumFitness += indiv.fitness
                if sumFitness >= randomValue:
                    if idx:
                        return num
                    else:
                        return indiv
        else: # If fitnessSum is zero, return a random individual
            if idx:
                return rnd.randint(0, len(self.population)-1)
            else:
                return rnd.sample(self.population, 1)
    def makeOffspring(self):
        '''Select two parents by fitness, cross over their genes, and return
        two offspring.'''
        offspringPop = []
        while len(offspringPop) < self.__offspringPopSize:
            parent1 = self.fitnessProportionateSelection()
            parent2 = parent1
            while parent2 == parent1:
                parent2 = self.fitnessProportionateSelection()
            offspring1, offspring2 = parent1.crossover(parent2)
            offspringPop.append(offspring1)
            if len(offspringPop) < self.__offspringPopSize:
                offspringPop.append(offspring2)
        return offspringPop
    def run(self, generations=20, outFile="GARun.txt"):
        '''Run the GA simulation for x generations. Print each generation's
        highest fitness to an output file.'''
        print ("Running Genetic Algorithm...")
        fd = open(outFile, "w")
        for i in range(generations):
            offspringPop = self.makeOffspring()
            for indiv in offspringPop:
                if self.__mutOffspring >= rnd.random():
                    indiv.mutate(self.__mutBit)
            self.population += offspringPop
            nextgen = []
            while len(nextgen) < self.__popSize:
                selectedidx = self.fitnessProportionateSelection(idx=True)
                selected = self.population.pop(selectedidx)
                nextgen.append(selected)
            self.population = nextgen
            strongest = max(self.population)
            print ("Generation",i+1,"highest fitness:",strongest.fitness)
            fd.write("Generation " + str(i+1) + ": " +\
                     str(strongest.fitness) + "\n")
        fd.close()
        strongest.env.printWorld()
        print ("...Done!")
   
def runGA():
    "Gets all GA parameters as user input and then runs it. No error checking!"
    popSize = raw_input("GA Population Size (Default 200):")
    if not popSize:
        popSize = 200
    else:
        popSize = int(popSize)
    offspringPopSize = raw_input("GA Offspring Population Size (Default 50):")
    if not offspringPopSize:
        offspringPopSize = 50
    else:
        offspringPopSize = int(offspringPopSize)
    mutOffspring = raw_input("Percent of offspring to mutate (Default 50):")
    if not mutOffspring:
        mutOffspring = 50.0
    else:
        mutOffspring = float(mutOffspring)
    mutBit = raw_input("Probability of a bit's mutation (Default 25):")
    if not mutBit:
        mutBit = 25.0
    else:
        mutBit = float(mutBit)
    generations = raw_input("Number of generations (Default 20):")
    if not generations:
        generations = 20
    else:
        generations = int(generations)
    worldName = raw_input("Name of world file for simulation (Default 'world1.txt'):")
    if not worldName:
        worldName = "world1.txt"
    outFile = raw_input("Name of output file (Default 'GARun.txt')")
    if not outFile:
        outFile = "GARun.txt"
    raw_input("Press enter to start the simulation.")
    sim = GA(popSize,offspringPopSize,mutOffspring,mutBit,worldName)
    sim.run(generations,outFile)
    
