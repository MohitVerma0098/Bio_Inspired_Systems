import random

def fitness(solution, values, weights, capacity):
    total_value = sum(v for v, s in zip(values, solution) if s == 1)
    total_weight = sum(w for w, s in zip(weights, solution) if s == 1)
    if total_weight > capacity:
        return 0
    return total_value

def levy_flight(Lambda):
    u = random.random()
    v = random.random()
    step = u ** (-1 / Lambda) * (v - 0.5)
    return step

def cuckoo_search(values, weights, capacity, n_nests=20, pa=0.25, alpha=1, Lambda=1.5, max_iter=100):
    n_items = len(values)
    nests = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(n_nests)]
    fitnesses = [fitness(n, values, weights, capacity) for n in nests]
    best_nest = nests[fitnesses.index(max(fitnesses))]

    for _ in range(max_iter):
        for i in range(n_nests):
            new_nest = nests[i][:]
            j = random.randint(0, n_items - 1)
            step = levy_flight(Lambda)
            if random.random() < 0.5:
                new_nest[j] = 1 - new_nest[j]
            if random.random() < abs(step):
                k = random.randint(0, n_items - 1)
                new_nest[k] = 1 - new_nest[k]
            new_fit = fitness(new_nest, values, weights, capacity)
            if new_fit > fitnesses[i]:
                nests[i] = new_nest
                fitnesses[i] = new_fit

        for i in range(n_nests):
            if random.random() < pa:
                nests[i] = [random.randint(0, 1) for _ in range(n_items)]
                fitnesses[i] = fitness(nests[i], values, weights, capacity)

        best_index = fitnesses.index(max(fitnesses))
        if fitnesses[best_index] > fitness(best_nest, values, weights, capacity):
            best_nest = nests[best_index]

    best_value = fitness(best_nest, values, weights, capacity)
    return best_nest, best_value

values = [60, 100, 120, 80, 30]
weights = [10, 20, 30, 40, 10]
capacity = 50

best_solution, best_value = cuckoo_search(values, weights, capacity)
print("Best solution:", best_solution)
print("Total value:", best_value)
