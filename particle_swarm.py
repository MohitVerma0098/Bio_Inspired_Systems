import random

def f(x):
    return -x**2 + 20*x + 5

def pso(max_iter=100, num_particles=30, w=0.7, c1=1.5, c2=1.5):
    particles = [random.uniform(-10, 30) for _ in range(num_particles)]
    velocities = [random.uniform(-1, 1) for _ in range(num_particles)]

    p_best = particles[:]
    p_best_values = [f(x) for x in particles]

    g_best = p_best[p_best_values.index(max(p_best_values))]
    g_best_value = max(p_best_values)

    for iteration in range(max_iter):
        for i in range(num_particles):
            r1, r2 = random.random(), random.random()
            velocities[i] = (w * velocities[i]
                             + c1 * r1 * (p_best[i] - particles[i])
                             + c2 * r2 * (g_best - particles[i]))
            particles[i] += velocities[i]
            fit = f(particles[i])
            if fit > p_best_values[i]:
                p_best[i] = particles[i]
                p_best_values[i] = fit

        best_particle_index = p_best_values.index(max(p_best_values))
        if p_best_values[best_particle_index] > g_best_value:
            g_best = p_best[best_particle_index]
            g_best_value = p_best_values[best_particle_index]

        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Best position = {g_best:.4f}, Best value = {g_best_value:.4f}")

    return g_best, g_best_value

best_x, best_val = pso()
print("\nOptimal x:", best_x)
print("Maximum f(x):", best_val)
