import random
import math

# --- Problem Setup ---

def euclidean_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(route, cities):
    distance = 0.0
    for i in range(len(route)):
        city_a = cities[route[i]]
        city_b = cities[route[(i + 1) % len(route)]]
        distance += euclidean_distance(city_a, city_b)
    return distance

# --- Gene Expression Algorithm (Simplified) ---

def create_individual(num_cities):
    # The "gene" is the permutation of cities
    return random.sample(range(num_cities), num_cities)

def mutate(individual):
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]
    return individual

def crossover(parent1, parent2):
    # Order crossover (OX)
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]

    ptr = end
    for gene in parent2:
        if gene not in child:
            if ptr >= len(parent1):
                ptr = 0
            child[ptr] = gene
            ptr += 1
    return child

def gene_expression_algorithm(cities, population_size=100, generations=500, mutation_rate=0.1):
    num_cities = len(cities)
    population = [create_individual(num_cities) for _ in range(population_size)]

    best_route = None
    best_distance = float('inf')

    for gen in range(generations):
        fitness = []
        for ind in population:
            dist = total_distance(ind, cities)
            fitness.append((dist, ind))
            if dist < best_distance:
                best_distance = dist
                best_route = ind.copy()

        # Selection (tournament)
        fitness.sort(key=lambda x: x[0])
        selected = [ind for _, ind in fitness[:population_size // 2]]

        # Crossover + Mutation
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)

        population = new_population

        if gen % 50 == 0:
            print(f"Generation {gen}: Best distance = {best_distance:.3f}")

    return best_route, best_distance

# --- Example Usage ---

if __name__ == "__main__":
    # Example cities (random coordinates)
    random.seed(42)
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(10)]

    best_route, best_distance = gene_expression_algorithm(cities)
    print("\nBest route found:", best_route)
    print("Best distance:", best_distance)
