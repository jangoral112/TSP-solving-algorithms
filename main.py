from generator import create_cities_coordinates
from tsp_algorithms import tsp_nearest_neighbor
from tsp_algorithms import tsp_brute_force_search, tsp_held_karp
from time import time

result_file = open("results.txt", "w")

number_of_measurements = 100

for cities_number in [10, 11, 12]:

    lists_of_coordinates = [create_cities_coordinates(cities_number, 2000, 2000) for i in range(number_of_measurements)]

    result_file.write(f"Results for {cities_number} cities and {number_of_measurements} measurements\n")

    brute_force_results = []

    start = time()
    for coordinates in lists_of_coordinates:
        _, result = tsp_brute_force_search(coordinates[0], coordinates[1:])
        brute_force_results.append(result)
    end = time()
    result_file.write(f"Average time for brute force algorithm in seconds: {(end-start)/number_of_measurements}\n")

    start = time()
    for coordinates in lists_of_coordinates:
        _, result = tsp_held_karp(coordinates[0], coordinates[1:])
    end = time()
    result_file.write(f"Average time for Held Karp algorithm in seconds: {(end-start)/number_of_measurements}\n")

    nearest_neighbor_results = []

    start = time()
    for coordinates in lists_of_coordinates:
        _, result = tsp_nearest_neighbor(coordinates[0], coordinates[1:])
        nearest_neighbor_results.append(result)
    end = time()

    result_file.write(f"Average time for nearest neighbor algorithm in seconds: {(end - start) / number_of_measurements}\n")
    relative_error_per_result = [abs(bf_result - nn_result)/bf_result
                                for bf_result, nn_result in zip(brute_force_results, nearest_neighbor_results)]

    average_relative_error = sum(relative_error_per_result)/number_of_measurements
    result_file.write(f"Average relative error for nearest neighbor algorithm : {average_relative_error}%\n")

    result_file.write("\n")

result_file.close()
