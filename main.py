from display import Display
from farm import Farm


def read_map(filename):
    file = open("config_files/" + filename)
    width, height = [int(i) for i in file.readline().split()[:2]]
    field_array = [[0 for x in range(width)] for y in range(height)]
    for y in range(height):
        row = file.readline().split()[:width]
        row = [int(i) for i in row]
        field_array[y] = row
    print(field_array)
    return field_array


if __name__ == '__main__':
    field = read_map("field_maps")
    farm = Farm(10, 5, 12, field=field)
    farm.print_field()
    display = Display(farm, 75)
    display.run()









