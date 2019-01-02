import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from world import World
from test_maps import rectangle, straight
from Agent import Agent, GeneAgent
import random

# Genetic algorithm specific
POPULATION_SIZE = 4
ELITE_SIZE = 2
MUTATION_RATE = 0.2
GENERATIONS = 100
MAX_STEPS = 1000

# Game state variables
world = World()
world.set_map(straight)
agents = []

gameEnd = True
populations = []
generationCount = 0
allRacerResults = {}

def CreateIndividual():
    p = []
    for i in range(MAX_STEPS):
        p.append(random.randint(0, 4))
    return p

def InitializePopulation(pSize):
    pop = []
    for i in range(pSize):
        pop.append(CreateIndividual())
    
    return pop

def RankPopulation(p):
    results = {}
    for pid in range(len(p)):
        score = allRacerResults[pid]

        candidates = []
        if score in results:
            candidates = results[score]
        candidates.append(pid)
        results[score] = candidates
    
    rankedPopulation = []
    for score in sorted(results, reverse=True):
        candidates = results[score]
        for candidate in candidates:
            rankedPopulation.append(p[candidate])
    
    return rankedPopulation

def SelectPopulation(pop, eSize):
    results = []
    for i in range(eSize):
        results.append(pop[i])
    
    shuffledPopulation = random.sample(pop, len(pop) - eSize)
    for s in shuffledPopulation:
        results.append(s)
    
    return results

def Breed(pop1, pop2):
    child = []
    for i in range(len(pop1)):
        if pop1[i] == pop2[i]:
            child.append(pop1[i])
        else:
            if random.random() < 0.5:
                child.append(pop1[i])
            else:
                child.append(pop2[i])
    
    return child

def BreedPopulation(selectedPopulation, eSize):
    children = []

    for i in range(eSize):
        children.append(selectedPopulation[i])
    
    for i in range(len(selectedPopulation) - eSize):
        children.append(Breed(selectedPopulation[i], selectedPopulation[len(selectedPopulation)-i-1]))
    
    return children

def Mutate(p, mRate):
    for mIndex in range(len(p)):
        if random.random() < mRate:
            p[mIndex] = random.randint(0, 4)
    
    return p

def MutatePopulation(population, mRate):
    mutatedPopulation = []
    for p in population:
        mutatedPopulation.append(Mutate(p, mRate))
    
    return mutatedPopulation

def NextGeneration(currGen, eSize, mRate):
    rankedPop = RankPopulation(currGen)
    selectedPop = SelectPopulation(rankedPop, eSize)
    children = BreedPopulation(selectedPop, eSize)
    nextGen = MutatePopulation(children, MUTATION_RATE)
    return nextGen

def PrintResult():
    print(f"Generation {generationCount}")

def gameUpdate(*args):
    global world
    global agents
    global populations
    global generationCount
    global gameEnd
    global allRacerResults

    if not gameEnd:
        state = world.get_state()
        actions=[agent.get_action(state) for agent in agents]
        allRacerResults = world.update(actions)
        if len(allRacerResults) != 0:
            gameEnd = True
    else:
        if populations == []:
            populations = InitializePopulation(POPULATION_SIZE)
        else:
            PrintResult()
            import time
            time.sleep(3)
            print("In pause")

            if generationCount < GENERATIONS:
                generationCount += 1
                populations = NextGeneration(populations, ELITE_SIZE, MUTATION_RATE)
            else:
                import os
                os._exit(0)
        
        world = World()
        world.set_map(straight)
        agents = []
        for i in range(POPULATION_SIZE):
            world.add_racer(0)
            world.racers[i].velocity=(0,1)
            agents.append(GeneAgent(populations[i]))
        
        gameEnd = False

    im.set_data(world.world_map)
    return im,

# Initialize renderer
screen = plt.figure()
im = plt.imshow(world.world_map, cmap='gray', vmin=0, vmax=255, animated=True)
ani = animation.FuncAnimation(screen, gameUpdate, frames=1000, interval=30, blit=False)
plt.show()