from random import randint
from typing import List


def create_cities_coordinates(number_of_cities: int, max_x: int, max_y: int, min_x: int = 0, min_y: int = 0) -> List[tuple]:
    cities_coordinates = []

    while len(cities_coordinates) < number_of_cities:

        x_coordinate = randint(min_x, max_x)
        y_coordinate = randint(min_y, max_y)
        coordinates = (x_coordinate, y_coordinate)

        if coordinates not in cities_coordinates:
            cities_coordinates.append(coordinates)

    return cities_coordinates
