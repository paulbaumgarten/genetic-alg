import random, json, logging, sys
from pprint import pprint

logging.basicConfig(filename='traveling_salesman.log', level=logging.DEBUG)

with open("travelling-salesman-data.json","r") as f:
    data = json.loads(f.read())

def get_distance_two_cities(city1, city2):
    n1 = data['names'].index(city1)
    n2 = data['names'].index(city2)
    distance = data['distances'][n1][n2]
    return distance

def get_distance_route(route):
    distance = 0
    for i in range(0, len(route)-1):
        city1 = route[i]
        city2 = route[i+1]
        distance = distance + get_distance_two_cities(city1, city2)
    return distance

def generate_random_1():
    # Generate 1 random member of the population
    route = "X"
    pool_of_names = data['names'][1:]
    while len(pool_of_names) > 0:
        pick = random.choice(pool_of_names)
        route = route + pick
        pool_of_names.remove(pick)
    route = route + "X"
    return route

def get_best(population, fitness):
    # Find the best member of the population
    best = 0
    best_score = 0
    for i in range(len(fitness)):
        if fitness[i] > best_score:
            best = i
            best_score = fitness[i]
    return population[best], get_distance_route(population[best])

def get_fitness(maybe):
    # Fitness score needs to be highest for best performers, hence using 1/distance
    return float(1 / get_distance_route(maybe))

def mating(parents):
    # Setup
    child = "X....................X" # a new child is born :) ... with no genes :(
    p1 = parents[0]
    p2 = parents[1]
    size_of_sequence = len(p1)//2
    start_of_sequence = random.randint(0, len(p1)//2)

    # Parent 1
    # Child goes from X....................X to X........aaaaaaaa....X (where a is genetic material from parent 1)
    for i in range(start_of_sequence, start_of_sequence+size_of_sequence):
        child = child[0:i] + p1[i] + child[i+1:]

    # Parent 2
    # Child goes from X........aaaaaaaa....X to X........aaaaaaaabbbbX (where b is genetic material from parent 2)
    p2_counter = start_of_sequence+size_of_sequence
    for i in range(start_of_sequence+size_of_sequence, len(child)-1):
        while p2[p2_counter] in child:
            p2_counter = (p2_counter + 1) % (len(p2))
        child = child[0:i] + p2[p2_counter] + child[i+1:]
    p2_counter = (p2_counter + 1) % (len(p2)-1)
    # Child goes from X........aaaaaaaabbbbX to XbbbbbbbbaaaaaaaabbbbX (where b is genetic material from parent 2)
    while "." in child:
        i = child.index(".")
        while p2[p2_counter] in child:
            p2_counter = (p2_counter + 1) % (len(p2))
        child = child[0:i] + p2[p2_counter] + child[i+1:]
    #print(child)
    return child

def mutation(original, mutation_likelihood, dna):
    child = original
    mutate_or_not = random.randint(0, mutation_likelihood)
    if mutate_or_not == 0:
        place_to_mutate = random.randint(1, len(child)-3)
        # Flip two genes... eg: .....AB.... becomes .....BA....
        child = child[0:place_to_mutate] + child[place_to_mutate+1] + child[place_to_mutate] + child[place_to_mutate+2:]
    return child

# --- MAIN ---
for attempt in range(100):
    # Setup
    population_size = 1000
    generation = 0                              # Generation number
    max_generations = 100000000                 # Abort after this number of generations
    max_generations_no_improvement = 1000000    # Abort if we have no improvement after this many generations
    score = 9999999999                          # Initial score of the best member of our population
    generations_since_improvement = 0
    logging.info(f"Attempt {attempt}")
    # Initial random population of children
    population = [generate_random_1() for i in range(population_size)]
    while generation < max_generations and generations_since_improvement < max_generations_no_improvement: 
        ### Process 1 generation ###
        # Fitness calculation - Get the fitness score for each member of the population
        fitness = [get_fitness(population[i]) for i in range (population_size)]
        # Record the best member of our current population
        best, score_new = get_best(population, fitness)
        ave = sum(fitness) / len(fitness)
        if score_new < score:
            score = score_new
            inf = f"Generation {generation}: The best is {best}, with score {score}. Generational mean is {int(1/ave)}"
            generations_since_improvement = 0
            logging.info(inf)
            print(inf)
        elif generation % 1000 == 0:
            inf = f"Generation {generation}: The best is {best}, with score {score}. Generational mean is {int(1/ave)}"
            print(inf)
        # Start a new generation
        new_generation = []
        # Hack: Let the best member live for another generation - Beawre of the risk of convergence
        # new_generation.append(best)
        # Create all new members of the new generation
        for i in range(population_size):
            # Parent selection - Randomly select two of the population members weighted according to their fitness
            parents = random.choices(population, weights=fitness, k=2)
            # Reproduction - Mating with cross over
            new_child = mating(parents)
            # Reproduction - Mutation
            new_child = mutation(new_child, 100, data['names']) # 1 in 50 = 2% chance of mutation
            # Add their offspring to the generation
            new_generation.append(new_child)
        # Move on to the next generation
        population = new_generation
        generation += 1
        generations_since_improvement += 1
