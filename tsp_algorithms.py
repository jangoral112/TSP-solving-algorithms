from typing import Set, List
from itertools import permutations, product, chain, combinations
from copy import deepcopy
import numpy as np


def tsp_brute_force_search(stating_city, cities_coordinates):

    all_cities = [stating_city] + cities_coordinates
    cities_number = len(all_cities)

    distance_matrix = calculate_distance_matrix(all_cities)

    routes = [(0,) + middle_cities + (0,) for middle_cities in permutations(range(1, cities_number))]

    routes_to_distances = dict()

    for route in routes:
        traveled_distance = 0
        for i in range(len(route) - 1):
            traveled_distance = traveled_distance + distance_matrix[route[i], route[i + 1]]
        routes_to_distances[route] = traveled_distance

    shortest_route_cities_indices = min(routes_to_distances, key=routes_to_distances.get)

    shortest_route = list(all_cities[index] for index in shortest_route_cities_indices)

    return shortest_route, routes_to_distances[shortest_route_cities_indices]


def tsp_held_karp(stating_city, cities_coordinates):
    all_cities = [stating_city, *cities_coordinates]

    cities_number = len(all_cities)
    distance_matrix = calculate_distance_matrix(all_cities)

    # key is tuple of end point and tuple representing set of points
    # value is distance to end point from given subset
    dp_dict = dict()

    # key is end point and tuple representing set of points
    # value is parent point to the end point
    parent_dict = dict()

    city_sets = list(power_set(range(1, cities_number)))[1:]
    final_set = city_sets[-1]
    city_sets = city_sets[:-1]

    for dest_city in range(1, cities_number):
        dp_dict[(dest_city, ())] = distance_matrix[0, dest_city]

    for city_set in city_sets:
        for dest_city in range(1, cities_number):

            if dest_city in city_set:
                continue

            distance, parent = shortest_path_from_city_set_to_city(dp_dict, distance_matrix, dest_city, city_set)
            parent_dict[(dest_city, city_set)] = parent
            dp_dict[(dest_city, city_set)] = distance

    distance, parent = shortest_path_from_city_set_to_city(dp_dict, distance_matrix, 0, final_set)
    parent_dict[(0, final_set)] = parent
    dp_dict[(0, final_set)] = distance

    shortest_route = get_shortest_route_indices(parent_dict, final_set)
    full_route = [all_cities[0]] + [all_cities[city_index] for city_index in reversed(shortest_route)]

    return full_route, dp_dict[0, final_set]


def tsp_nearest_neighbor(stating_city, cities_coordinates):
    all_cities = [stating_city, *cities_coordinates]

    distance_matrix = calculate_distance_matrix(all_cities)
    cities_number = len(all_cities)

    visited_cities = [0]
    not_visited_cities = list(range(1, cities_number))
    total_distance = 0

    while len(visited_cities) < cities_number:
        min_distance = distance_matrix[not_visited_cities[0], visited_cities[-1]]
        next_city = not_visited_cities[0]

        for city in not_visited_cities[1:]:
            if min_distance > distance_matrix[city, visited_cities[-1]]:
                min_distance = distance_matrix[city, visited_cities[-1]]
                next_city = city

        total_distance += min_distance
        visited_cities.append(next_city)
        not_visited_cities.remove(next_city)

    total_distance += distance_matrix[visited_cities[-1], 0]

    return [all_cities[city_index] for city_index in visited_cities] + [stating_city], total_distance


def calculate_distance_matrix(coordinates):
    cities_number = len(coordinates)

    distance_matrix = np.zeros((cities_number, cities_number))

    for i, j in product(range(cities_number), range(cities_number)):
        distance_matrix[i, j] = distance_between(coordinates[i], coordinates[j])

    return distance_matrix


def distance_between(point_one: tuple, point_two: tuple):
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5


def shortest_path_from_city_set_to_city(dp_dict, distance_matrix, dest_city, city_set):
    parents_to_routes_distances = dict()

    for city_before_dest in city_set:
        previous_cities = tuple(x for x in city_set if x != city_before_dest)
        total_distance = distance_matrix[dest_city, city_before_dest] + dp_dict.get((city_before_dest, previous_cities))
        parents_to_routes_distances[city_before_dest] = total_distance

    parent = min(parents_to_routes_distances, key=parents_to_routes_distances.get)
    route_distance = parents_to_routes_distances[parent]

    return route_distance, parent


def get_shortest_route_indices(parent_dict, final_set):
    temp_set = deepcopy(final_set)
    shortest_route = [0]
    current_city = 0
    while temp_set != ():
        predecessor = parent_dict[(current_city, temp_set)]
        shortest_route.append(predecessor)
        current_city = predecessor
        temp_set = tuple(city for city in temp_set if city != predecessor)

    return shortest_route


def power_set(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

