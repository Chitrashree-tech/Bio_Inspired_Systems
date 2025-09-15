import numpy as np
import math

# ---------------------------
# Objective Function (minimize)
# ---------------------------
def objective_function(x):
    return np.sum(x**2)  # Sphere function example

# ---------------------------
# Lévy flight step
# ---------------------------
def levy_flight(Lambda, size):
    sigma = (math.gamma(1+Lambda) * math.sin(math.pi*Lambda/2) /
             (math.gamma((1+Lambda)/2) * Lambda * 2**((Lambda-1)/2)))**(1/Lambda)
    u = np.random.normal(0, sigma, size)
    v = np.random.normal(0, 1, size)
    return u / (np.abs(v)**(1/Lambda))

# ---------------------------
# Cuckoo Search Algorithm
# ---------------------------
def cuckoo_search(n=10, dim=2, lb=-10, ub=10, pa=0.25, max_iter=50):
    # Initialize nests randomly
    nests = np.random.uniform(lb, ub, (n, dim))
    fitness = np.array([objective_function(x) for x in nests])
    best_nest = nests[np.argmin(fitness)].copy()
    best_fitness = np.min(fitness)

    for t in range(max_iter):
        # Generate new solutions via Lévy flights
        new_nests = nests + levy_flight(1.5, (n, dim)) * (nests - best_nest)
        new_nests = np.clip(new_nests, lb, ub)  # keep within bounds
        new_fitness = np.array([objective_function(x) for x in new_nests])

        # Replace nests if better
        for i in range(n):
            if new_fitness[i] < fitness[i]:
                nests[i] = new_nests[i]
                fitness[i] = new_fitness[i]

        # Abandon some nests (with probability pa)
        abandon = np.random.rand(n) < pa
        nests[abandon] = np.random.uniform(lb, ub, (np.sum(abandon), dim))
        fitness[abandon] = [objective_function(x) for x in nests[abandon]]

        # Update global best
        if np.min(fitness) < best_fitness:
            best_fitness = np.min(fitness)
            best_nest = nests[np.argmin(fitness)].copy()

        print(f"Iteration {t+1}: Best Fitness = {best_fitness:.6f}")

    return best_nest, best_fitness

# ---------------------------
# Run the algorithm
# ---------------------------
best_solution, best_value = cuckoo_search()
print("\nBest Solution:", best_solution)
print("Best Value:", best_value)
