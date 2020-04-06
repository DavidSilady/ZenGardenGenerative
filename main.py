from display import Display
from farm import Farm

if __name__ == '__main__':
    farm = Farm(10, 5, 12)
    farm.print_field()
    display = Display(farm, 75)
    display.run()







