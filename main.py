import random
from display import Display
from farm import Farm
from frick_chamber import Subject, Generation
from monk import Monk, Instruction

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def read_map(filename):
    file = open("config_files/" + filename)
    map_width, map_height = [int(i) for i in file.readline().split()[:2]]
    field_array = [[0 for x in range(map_width)] for y in range(map_height)]
    for y in range(map_height):
        row = file.readline().split()[:map_width]
        row = [int(i) for i in row]
        field_array[y] = row
    print(field_array)
    return field_array, map_width, map_height


if __name__ == '__main__':
    # field, width, height = read_map("map")
    # farm = Farm(width, height, field=field)
    farm = Farm(20, 20, 10)
    farm.print_field()
    monk = Monk(farm)
    generation = Generation(farm)
    print(generation.average_fitness)
    best_gen = generation
    next_gen = generation

    avg_function = []
    best_function = []
    index = 0
    f = open("animation/fitness.txt", "w")
    f.write("")
    f.close()
    f = open("animation/avg_fitness.txt", "w")
    f.write("")
    f.close()
    for _ in range(15000):
        next_gen = Generation(farm, generation)
        # print(index, next_gen.get_best_subject().fitness, next_gen.average_fitness)
        index += 1
        avg_function.append(next_gen.average_fitness)
        best_function.append(next_gen.get_best_subject().fitness)
        if next_gen.average_fitness > best_gen.average_fitness:
            best_gen = next_gen
        f = open("animation/fitness.txt", "a")
        f.write(str(index) + " " + str(next_gen.get_best_subject().fitness) + "\n")
        f.close()
        f = open("animation/avg_fitness.txt", "a")
        f.write(str(index) + " " + str(next_gen.average_fitness) + "\n")
        f.close()
        if next_gen.get_best_subject().fitness == farm.width*farm.height:
            break
        generation = next_gen

    best_subject = next_gen.get_best_subject()
    next_gen.print_all_fitness()
    print("Last best subject:", best_subject.calculate_fitness())
    # print(farm.count_fitness())
    # display = Display(best_subject.monk.farm, 75, best_subject.monk)
    # display.run()













