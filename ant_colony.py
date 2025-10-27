import numpy as np
import random

def ant_colony_optimization(distance_matrix, n_ants=20, n_iterations=100, alpha=1, beta=5, rho=0.5, Q=100):
    n_cities = len(distance_matrix)
    pheromone = np.ones((n_cities, n_cities))
    best_distance = float('inf')
    best_path = None

    for iteration in range(n_iterations):
        all_paths = []
        all_distances = []

        for ant in range(n_ants):
            visited = [random.randint(0, n_cities - 1)]
            while len(visited) < n_cities:
                current_city = visited[-1]
                probabilities = []
                for next_city in range(n_cities):
                    if next_city not in visited:
                        tau = pheromone[current_city][next_city] ** alpha
                        eta = (1 / distance_matrix[current_city][next_city]) ** beta
                        probabilities.append(tau * eta)
                    else:
                        probabilities.append(0)
                probabilities = np.array(probabilities)
                if probabilities.sum() == 0:
                    next_city = random.choice([i for i in range(n_cities) if i not in visited])
                else:
                    probabilities /= probabilities.sum()
                    next_city = np.random.choice(range(n_cities), p=probabilities)
                visited.append(next_city)

            visited.append(visited[0])
            total_distance = sum(distance_matrix[visited[i]][visited[i + 1]] for i in range(n_cities))
            all_paths.append(visited)
            all_distances.append(total_distance)

            if total_distance < best_distance:
                best_distance = total_distance
                best_path = visited

        pheromone *= (1 - rho)
        for path, dist in zip(all_paths, all_distances):
            for i in range(n_cities):
                pheromone[path[i]][path[i + 1]] += Q / dist

        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Best distance = {best_distance:.3f}")

    return best_path, best_distance

distance_matrix = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

best_path, best_distance = ant_colony_optimization(distance_matrix)
print("\nShortest route:", best_path)
print("Shortest distance:", best_distance)
