
"""
Worked will when goal was 'ilovecs'.
I changed it to "computer science is pretty cool" but within just a few generations it converged around 67-70%
    Generation 6794 best is compitzo s hence is awitty  oo  score 0.6774193548387096
    Generation 6795 best is computvd mhidnce is uyatty dooz score 0.6774193548387096
    Generation 6796 best is computdr shhenke is nwattyl ooz score 0.6774193548387096
    Generation 6797 best is computvh ahidnce is uyatty booz score 0.6774193548387096
    Generation 6798 best is computdr sxhence is nwitwyo ooj score 0.6774193548387096
    Generation 6799 best is computgg bhidnce is uratty dooz score 0.7096774193548387
    Generation 6800 best is computtr slhlnce is awatby  ooz score 0.6774193548387096
    Generation 6801 best is komputed mkience iw sygtty door score 0.6774193548387096
A better approach to fitness selection is required
"""

import random
from pprint import pprint

dna = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']

def generate_random(size):# Create a random population of N elements
    letters = [random.choice(dna) for letter in range(size)]
    return "".join(letters)

def get_best(population, fitness):
    best = 0
    best_score = 0
    for i in range(len(fitness)):
        if fitness[i] > best_score:
            best = i
            best_score = fitness[i]
    return population[best], best_score

def get_fitness(maybe, goal):
    points = 0
    for i in range(len(goal)):
        if maybe[i] == goal[i]:
            points += 1
    return float(points / len(goal))

def mating(parents):
    new_child = "" # a new child is born :) ... with no genes :(
    for gene in range(len(parents[0])): # for all the genes
        if gene % 2 == 0: # select alternate genes from each parent
            new_child = new_child + parents[0][gene]
        else:
            new_child = new_child + parents[1][gene]
    return new_child

def mutation(original, mutation_likelihood):
    child = ""
    for gene in range(len(original)):
        mutate_or_not = random.randint(0, mutation_likelihood)
        if mutate_or_not == 0:
            child = child + random.choice(dna) # Pick a random gene from the genepool
        else:
            child = child + original[gene] # Keep the existing gene
    return child

# --- MAIN ---
if __name__ == "__main__":
    # Set our goal
    goal = "computer science is pretty cool"
    # Initial random population of 1000 children
    population = [generate_random(len(goal)) for i in range(1000)]
    print("Inital population:",population)
    n = 0 # generation number
    score = 0 # score of the best member of our population
    while n < 10000 and score<0.99999: # Loop over our cohort
        # Fitness calculation - Get the fitness score for each member of the population
        fitness = [get_fitness(population[i], goal) for i in range (1000)]
        # Out of interest, who are the best members of our population?
        best, score = get_best(population, fitness)
        print("Generation",n,"best is",best,"score",score)
        # Start a new generation
        new_generation = []
        for i in range(1000):
            # Parent selection - Randomly select two of the population members weighted according to their fitness
            parents = random.choices(population, weights=fitness, k=2)
            # Reproduction - Mating with cross over
            new_child = mating(parents)
            # Reproduction - Mutation
            new_child = mutation(new_child, 50) # 1 in 50 = 2% chance of mutation
            # Offspring
            new_generation.append(new_child)
        # Move on to the next generation
        population = new_generation
        n += 1
