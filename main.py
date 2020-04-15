import random

from display import Display
from farm import Farm
from frick_chamber import Subject
from monk import Monk, Instruction


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
    farm = Farm(20, 20, 20)
    farm.print_field()
    monk = Monk(farm)
    mother = Subject(farm)
    father = Subject(farm)
    kid = Subject(farm, mother, father)
    child = Subject(farm, father, mother)
    mother.print_instructions()
    print("end")
    father.print_instructions()
    print("end")
    kid.print_instructions()
    print(mother.calculate_fitness())
    print(father.calculate_fitness())
    print(kid.calculate_fitness())
    print(child.calculate_fitness())
    # print(farm.count_fitness())
    # display = Display(farm, 75, monk)
    # display.run()









