import random

# Travelling Salesman Problem using Genetic Algorithm

cities = ["A", "B", "C", "D", "E"]

# Distance between cities
distance = {
    "A": {"A": 0, "B": 10, "C": 15, "D": 20, "E": 18},
    "B": {"A": 10, "B": 0, "C": 35, "D": 25, "E": 30},
    "C": {"A": 15, "B": 35, "C": 0, "D": 30, "E": 20},
    "D": {"A": 20, "B": 25, "C": 30, "D": 0, "E": 15},
    "E": {"A": 18, "B": 30, "C": 20, "D": 15, "E": 0}
}

POPULATION_SIZE = 20
GENERATIONS = 100
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.8


# Create a random route
def create_route():
    route = cities[:]
    random.shuffle(route)
    return route


# Create initial population
def create_population():
    return [create_route() for _ in range(POPULATION_SIZE)]


# Calculate total distance of a route
def route_distance(route):
    total = 0

    for i in range(len(route)):
        current = route[i]
        next_city = route[(i + 1) % len(route)]
        total += distance[current][next_city]

    return total


# Calculate fitness
def fitness(route):
    return 1 / route_distance(route)


# Selection using tournament selection
def selection(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)

    if fitness(parent1) > fitness(parent2):
        return parent1[:]
    else:
        return parent2[:]


# Order Crossover
def crossover(parent1, parent2):

    if random.random() > CROSSOVER_RATE:
        return parent1[:]

    start, end = sorted(
        random.sample(range(len(cities)), 2)
    )

    child = [None] * len(cities)

    # Copy part of parent 1
    child[start:end] = parent1[start:end]

    # Fill remaining positions from parent 2
    remaining = [city for city in parent2 if city not in child]

    j = 0

    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1

    return child


# Mutation using swap
def mutate(route):

    if random.random() < MUTATION_RATE:

        i, j = random.sample(range(len(route)), 2)

        route[i], route[j] = route[j], route[i]


# Genetic Algorithm
def genetic_algorithm():

    population = create_population()

    best_route = None
    best_distance = float("inf")

    for generation in range(GENERATIONS):

        # Evaluate population
        for route in population:

            current_distance = route_distance(route)

            if current_distance < best_distance:
                best_distance = current_distance
                best_route = route[:]

        # Create next generation
        new_population = []

        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)

            mutate(child)

            new_population.append(child)

        population = new_population

        print(
            "Generation:", generation + 1,
            "Best Route:", best_route,
            "Distance:", best_distance
        )

    return best_route, best_distance


# Run the algorithm
best_route, best_distance = genetic_algorithm()


# Final result
print("\nFinal Result")
print("Best Route:", " -> ".join(best_route + [best_route[0]]))
print("Shortest Distance:", best_distance, "km")
