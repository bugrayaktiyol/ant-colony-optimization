import random
import matplotlib.pyplot as plt
import networkx as nx

def calculate_total_distance(route, distance_matrix):
    total_dist = 0
    for i in range(len(route)):
        total_dist += distance_matrix[route[i-1]][route[i]]
    return total_dist

def initialize_pheromone_matrix(num_cities, initial_pheromone):
    pheromone_matrix = [[initial_pheromone] * num_cities for _ in range(num_cities)]
    return pheromone_matrix

def update_pheromones(pheromone_matrix, ant_routes, distance_matrix, decay_rate):
    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix[i])):
            pheromone_matrix[i][j] *= (1 - decay_rate)

    for route in ant_routes:
        total_distance = calculate_total_distance(route, distance_matrix)
        for i in range(len(route)):
            pheromone_matrix[route[i-1]][route[i]] += 1.0 / total_distance

def pick_next_city(current_city, pheromone_matrix, distance_matrix, alpha, beta):
    pheromones = pheromone_matrix[current_city]
    distances = distance_matrix[current_city]
    city_probabilities = []

    for i in range(len(pheromones)):
        if distances[i] == 0:
            city_probabilities.append(0)
        else:
            city_probabilities.append((pheromones[i] ** alpha) * ((1.0 / distances[i]) ** beta))

    total_probability = sum(city_probabilities)
    normalized_probabilities = [prob / total_probability for prob in city_probabilities]

    next_city = random.choices(range(len(pheromones)), weights=normalized_probabilities)[0]
    return next_city

def ant_colony_optimization_with_history(distance_matrix, num_ants, num_iterations, alpha, beta, decay_rate, initial_pheromone=1.0):
    num_cities = len(distance_matrix)
    pheromone_matrix = initialize_pheromone_matrix(num_cities, initial_pheromone)

    best_route = None
    best_distance = float('inf')
    distance_history = []

    for _ in range(num_iterations):
        ant_routes = []
        for _ in range(num_ants):
            route = [random.randint(0, num_cities - 1)]
            while len(route) < num_cities:
                next_city = pick_next_city(route[-1], pheromone_matrix, distance_matrix, alpha, beta)
                if next_city not in route:
                    route.append(next_city)
            route.append(route[0])
            ant_routes.append(route)

            route_distance = calculate_total_distance(route, distance_matrix)
            if route_distance < best_distance:
                best_route = route
                best_distance = route_distance

        update_pheromones(pheromone_matrix, ant_routes, distance_matrix, decay_rate)

        distance_history.append(best_distance)

    return best_route, best_distance, distance_history


def plot_distance_history(distance_history):
    plt.figure(figsize=(8, 6))
    plt.plot(distance_history, marker='o', linestyle='-', color='b')
    plt.title('Change of Fitness')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.show()

def plot_graph(best_route, distance_matrix, locations):
    G = nx.Graph()

    for i, location in enumerate(locations):
        G.add_node(i, label=location)

    for i in range(len(best_route) - 1):
        city1 = best_route[i]
        city2 = best_route[i + 1]
        distance = distance_matrix[city1][city2]
        G.add_edge(city1, city2, weight=distance)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), font_size=6, node_size=300)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', font_size=6)
    plt.show()