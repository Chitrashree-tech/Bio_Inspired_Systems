import random
import math

# -------------------------
# Problem Setup (TSP Cities)
# -------------------------
cities = {
    0: (0, 0),
    1: (1, 5),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3)
}

num_cities = len(cities)

# Distance matrix
distances = [[0] * num_cities for _ in range(num_cities)]
for i in range(num_cities):
    for j in range(num_cities):
        xi, yi = cities[i]
        xj, yj = cities[j]
        distances[i][j] = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

# -------------------------
# Parameters
# -------------------------
num_ants = 10
iterations = 50
alpha = 0      # pheromone importance
beta = 5.0       # heuristic importance
rho = 0.5        # evaporation rate
Q = 5        # pheromone deposit factor
initial_pheromone = 1.0

# -------------------------
# Initialize pheromones
# -------------------------
pheromone = [[initial_pheromone] * num_cities for _ in range(num_cities)]

# -------------------------
# Helper Functions
# -------------------------
def tour_length(tour):
    length = 0
    for i in range(len(tour) - 1):
        length += distances[tour[i]][tour[i + 1]]
    length += distances[tour[-1]][tour[0]]  # return to start
    return length

def select_next_city(current, unvisited):
    probabilities = []
    denom = sum((pheromone[current][j] ** alpha) * ((1 / distances[current][j]) ** beta) for j in unvisited)
    for j in unvisited:
        prob = (pheromone[current][j] ** alpha) * ((1 / distances[current][j]) ** beta) / denom
        probabilities.append((j, prob))

    # Roulette wheel selection
    r = random.random()
    cumulative = 0
    for city, prob in probabilities:
        cumulative += prob
        if r <= cumulative:
            return city
    return unvisited[-1]

# -------------------------
# Main ACO Loop
# -------------------------
best_length = float("inf")
best_tour = None

for it in range(iterations):
    all_tours = []
    all_lengths = []

    for ant in range(num_ants):
        start = random.randint(0, num_cities - 1)
        tour = [start]
        unvisited = list(set(range(num_cities)) - {start})

        while unvisited:
            current = tour[-1]
            next_city = select_next_city(current, unvisited)
            tour.append(next_city)
            unvisited.remove(next_city)

        length = tour_length(tour)
        all_tours.append(tour)
        all_lengths.append(length)

        if length < best_length:
            best_length = length
            best_tour = tour[:]

    # Evaporate pheromones
    for i in range(num_cities):
        for j in range(num_cities):
            pheromone[i][j] *= (1 - rho)

    # Deposit pheromones (each ant contributes)
    for tour, length in zip(all_tours, all_lengths):
        for i in range(len(tour) - 1):
            a, b = tour[i], tour[i + 1]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length
        # close the tour
        pheromone[tour[-1]][tour[0]] += Q / length
        pheromone[tour[0]][tour[-1]] += Q / length

    print(f"Iteration {it+1}: Best Length = {best_length}, Best Tour = {best_tour}")

# -------------------------
# Final Result
# -------------------------
print("\nFinal Best Tour:", best_tour)
print("Final Best Length:", best_length)
