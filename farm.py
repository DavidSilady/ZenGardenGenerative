import random


class Farm:
	def __init__(self, width, height, num_obstacles=0, field=None):
		self.width = width
		self.height = height
		self.field = field
		if field is None:
			self.field = self.generate_field(num_obstacles)

	def clear(self):
		for y in range(self.height):
			for x in range(self.width):
				if self.field[y][x] > 0:
					self.field[y][x] = 0

	def generate_field(self, num_obstacles):
		# -1 = not accessible / rock / obstacle
		# 0 = not visited
		field_array = [[0 for x in range(self.width)] for y in range(self.height)]
		obstacle_array = [0 for i in range(self.width * self.height)]

		for i in range(num_obstacles):
			obstacle_array[i] = -1
		random.shuffle(obstacle_array)

		index = 0
		for y in range(self.height):
			for x in range(self.width):
				field_array[y][x] = obstacle_array[index]
				index += 1

		return field_array

	def print_field(self):
		for y in range(self.height):
			output = ""
			for x in range(self.width):
				if self.field[y][x] == -1:
					output += "k "
				else:
					output += str(self.field[y][x]) + " "
			print(output)

	def count_fitness(self):
		fitness = 0
		for y in range(self.height):
			for x in range(self.width):
				if not self.field[y][x] == 0:
					fitness += 1
		return fitness
