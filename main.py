from display import Display
from farm import Farm
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
    field, width, height = read_map("map")
    farm = Farm(width, height, field=field)
    # farm = Farm(5, 3, 4)
    farm.print_field()
    monk = Monk(farm)
    monk.enter_field(Instruction(8, ["right", "left"]))
    monk.enter_field(Instruction(5, ["right", "left"]))
    farm.print_field()
    # display = Display(farm, 75, monk)
    # display.run()









