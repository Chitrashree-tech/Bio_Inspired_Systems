import random

# Step 1: Define function (to maximize)
def f(x):
    return (x**2+3*x+4)   # simple quadratic

# Step 2: Parameters
num_particles = 10
iterations = 20
w = 0.4# inertia
c1, c2 = 1.5, 1

# Step 3: Initialize particles
positions = [random.uniform(-10, 10) for _ in range(num_particles)]
velocities = [random.uniform(-1, 1) for _ in range(num_particles)]
pbest = positions[:]
pbest_val = [f(x) for x in positions]
gbest = pbest[pbest_val.index(max(pbest_val))]

# Step 4–6: Iterate
for _ in range(iterations):
    for i in range(num_particles):
        # Update velocity
        velocities[i] = (w*velocities[i] 
                         + c1*random.random()*(pbest[i]-positions[i])
                         + c2*random.random()*(gbest-positions[i]))
        # Update position
        positions[i] += velocities[i]

        # Update personal best
        val = f(positions[i])
        if val > pbest_val[i]:
            pbest[i] = positions[i]
            pbest_val[i] = val

    # Update global best
    gbest = pbest[pbest_val.index(max(pbest_val))]

# Step 7: Output
print("Global Best solution:", gbest, "Fitness Value:", f(gbest))
