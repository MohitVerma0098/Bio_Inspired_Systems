import numpy as np
import random

def fitness(assignment, distance_matrix):
    total = 0
    for car, slot in enumerate(assignment):
        total += distance_matrix[car][slot]
    return total

def repair(assignment):
    n = len(assignment)
    unique = list(set(assignment))
    missing = [i for i in range(n) if i not in unique]
    seen = set()
    duplicates = [x for x in assignment if x in seen or seen.add(x)]
    for i in range(len(assignment)):
        if assignment[i] in duplicates:
            assignment[i] = missing.pop(0)
            duplicates.remove(assignment[i])
    return assignment

def grey_wolf_optimization(distance_matrix, n_wolves=20, max_iter=100, a_decay=2):
    n = len(distance_matrix)
    wolves = [np.random.permutation(n).tolist() for _ in range(n_wolves)]
    fitnesses = [fitness(w, distance_matrix) for w in wolves]

    alpha = wolves[np.argmin(fitnesses)]
    beta = wolves[np.argsort(fitnesses)[1]]
    delta = wolves[np.argsort(fitnesses)[2]]

    for t in range(max_iter):
        a = a_decay - t * (a_decay / max_iter)
        for i in range(n_wolves):
            X1, X2, X3 = [], [], []
            for j in range(n):
                r1, r2 = random.random(), random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[j] - wolves[i][j])
                X1.append(alpha[j] - A1 * D_alpha)

                r1, r2 = random.random(), random.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta[j] - wolves[i][j])
                X2.append(beta[j] - A2 * D_beta)

                r1, r2 = random.random(), random.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta[j] - wolves[i][j])
                X3.append(delta[j] - A3 * D_delta)

            new_pos = [(X1[j] + X2[j] + X3[j]) / 3 for j in range(n)]
            new_pos = np.argsort(new_pos).tolist()
            new_pos = repair(new_pos)
            new_fit = fitness(new_pos, distance_matrix)
            if new_fit < fitnesses[i]:
                wolves[i] = new_pos
                fitnesses[i] = new_fit

        sorted_idx = np.argsort(fitnesses)
        alpha, beta, delta = wolves[sorted_idx[0]], wolves[sorted_idx[1]], wolves[sorted_idx[2]]
        if t % 10 == 0:
            print(f"Iteration {t}: Best distance = {fitnesses[sorted_idx[0]]:.3f}")

    best = alpha
    best_fit = fitness(best, distance_matrix)
    return best, best_fit

distance_matrix = np.array([
    [10, 15, 20, 25],
    [12, 9, 27, 30],
    [18, 24, 6, 11],
    [14, 19, 17, 13]
])

best_assignment, best_distance = grey_wolf_optimization(distance_matrix)
print("\nBest assignment (car → slot):", best_assignment)
print("Minimum total walking distance:", best_distance)
