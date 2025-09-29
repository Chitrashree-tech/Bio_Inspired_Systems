import numpy as np

# Objective Function (Sphere function)
def objective_function(x):
    return np.sum(x**2)

# Grey Wolf Optimizer
def grey_wolf_optimizer(obj_func, dim=2, search_agents=10, max_iter=50, lb=-10, ub=10):
    # Initialize wolf positions randomly
    wolves = np.random.uniform(lb, ub, (search_agents, dim))
    fitness = np.array([obj_func(w) for w in wolves])

    # Identify alpha, beta, delta wolves
    alpha, beta, delta = np.zeros(dim), np.zeros(dim), np.zeros(dim)
    alpha_score, beta_score, delta_score = float("inf"), float("inf"), float("inf")

    # Find initial alpha, beta, delta
    for i in range(search_agents):
        if fitness[i] < alpha_score:
            alpha_score = fitness[i]
            alpha = wolves[i].copy()
        elif fitness[i] < beta_score:
            beta_score = fitness[i]
            beta = wolves[i].copy()
        elif fitness[i] < delta_score:
            delta_score = fitness[i]
            delta = wolves[i].copy()

    # Main loop
    for t in range(max_iter):
        a = 2 - t * (2 / max_iter)  # linearly decreases from 2 to 0

        for i in range(search_agents):
            for j in range(dim):
                r1, r2 = np.random.rand(), np.random.rand()

                A1, C1 = 2 * a * r1 - a, 2 * r2
                D_alpha = abs(C1 * alpha[j] - wolves[i][j])
                X1 = alpha[j] - A1 * D_alpha

                r1, r2 = np.random.rand(), np.random.rand()
                A2, C2 = 2 * a * r1 - a, 2 * r2
                D_beta = abs(C2 * beta[j] - wolves[i][j])
                X2 = beta[j] - A2 * D_beta

                r1, r2 = np.random.rand(), np.random.rand()
                A3, C3 = 2 * a * r1 - a, 2 * r2
                D_delta = abs(C3 * delta[j] - wolves[i][j])
                X3 = delta[j] - A3 * D_delta

                wolves[i][j] = (X1 + X2 + X3) / 3  # update wolf position

            # Boundaries
            wolves[i] = np.clip(wolves[i], lb, ub)

            # Fitness evaluation
            score = obj_func(wolves[i])

            if score < alpha_score:
                delta_score, delta = beta_score, beta.copy()
                beta_score, beta = alpha_score, alpha.copy()
                alpha_score, alpha = score, wolves[i].copy()
            elif score < beta_score:
                delta_score, delta = beta_score, beta.copy()
                beta_score, beta = score, wolves[i].copy()
            elif score < delta_score:
                delta_score, delta = score, wolves[i].copy()

        print(f"Iteration {t+1}: Best Fitness = {alpha_score:.6f}")

    return alpha, alpha_score

# Run GWO
best_position, best_value = grey_wolf_optimizer(objective_function, dim=2, search_agents=15, max_iter=50)
print("\nBest Position:", best_position)
print("Best Fitness:", best_value)
