from typing import List
from farm import Farm


class Instruction:
	def __init__(self, starting_point, strategy, strategy_index=-1):
		self.starting_point = starting_point
		self.strategy = strategy  # right/left
		self.strategy_index = strategy_index

	def reset(self, index=1):
		self.strategy_index = index
		return self

	def get_starting_coordinates(self, farm):
		start_index = 0
		start_index += self.starting_point
		if start_index < farm.width:  # Top row
			return start_index, 0, "top"
		start_index -= farm.width
		if start_index < farm.height:  # Right column
			return farm.width - 1, start_index, "right"
		start_index -= farm.height
		if start_index < farm.height:  # Left column
			return 0, start_index, "left"
		if start_index < farm.width:  # Bottom row
			return start_index, farm.height - 1, "bottom"
		return -1, -1, "none"

	def print_instruction(self, farm):
		print(self.get_starting_coordinates(farm))
		print(self.strategy)

	def get_next_strategy(self):
		self.strategy_index += 1
		return self.strategy[self.strategy_index % len(self.strategy)]


class Monk:
	def __init__(self, farm: Farm):
		self.farm = farm
		self.num_enters = 1
		self.x = -1
		self.y = -1

	def step_on_tile(self):
		if self.is_in_field():
			self.farm.field[self.y][self.x] = self.num_enters

	def is_in_field(self):
		if 0 <= self.x < self.farm.width:
			if 0 <= self.y < self.farm.height:
				return True
		return False

	def is_clear_way(self, new_x, new_y):
		"""
		:return: bool if the next step is clear (doesn't contain an obstacle)
		"""
		if new_x < 0 or new_x >= self.farm.width:
			return True
		if new_y < 0 or new_y >= self.farm.height:
			return True
		if self.farm.field[new_y][new_x] == 0:
			return True
		# print("Obstacle in the way!", new_x, new_y)
		return False

	def move_up(self):
		new_x = self.x
		new_y = self.y - 1
		if new_y < 0:
			# print("Out of field.")
			if new_y < -1:
				return 0, 0
			if self.is_in_field():
				self.num_enters += 1
			self.y = new_y
			return 0, -1
		if not self.is_clear_way(new_x, new_y):
			return 0, 0
		self.y = new_y
		self.step_on_tile()
		return 0, -1

	def move_down(self):
		new_x = self.x
		new_y = self.y + 1
		if new_y >= self.farm.height:
			# print("Out of field.")
			if new_y >= self.farm.height + 1:
				return 0, 0
			if self.is_in_field():
				self.num_enters += 1
			self.y = new_y
			return 0, 1
		if not self.is_clear_way(new_x, new_y):
			return 0, 0
		self.y = new_y
		self.step_on_tile()
		return 0, 1

	def move_right(self):
		new_x = self.x + 1
		new_y = self.y
		if new_x >= self.farm.width:
			# print("Out of field.")
			if new_x >= self.farm.width + 1:
				return 0, 0
			if self.is_in_field():
				self.num_enters += 1
			self.x = new_x
			return 1, 0
		if not self.is_clear_way(new_x, new_y):
			return 0, 0
		self.x = new_x
		self.step_on_tile()
		return 1, 0

	def move_left(self):
		new_x = self.x - 1
		new_y = self.y
		if new_x < 0:
			# print("Out of field.")
			if new_x < -1:
				return 0, 0
			if self.is_in_field():
				self.num_enters += 1
			self.x = new_x
			return -1, 0
		if not self.is_clear_way(new_x, new_y):
			return 0, 0
		self.x = new_x
		self.step_on_tile()
		return -1, 0

	def vertical_sweep(self, y_offset, instruction: Instruction):
		if self.is_stuck(0, y_offset):
			# print("Got stuck.", self.x, self.y)
			return -1
		if not self.is_clear_way(self.x, self.y + y_offset):
			if not self.is_in_field():
				# print("Cant't enter. . .")
				return 1
			if instruction.get_next_strategy() == "right":
				if self.is_clear_way(self.x - y_offset, self.y):
					return self.horizontal_sweep(x_offset=-y_offset, instruction=instruction)
				else:
					return self.horizontal_sweep(x_offset=y_offset, instruction=instruction)
			else:
				if self.is_clear_way(self.x + y_offset, self.y):
					return self.horizontal_sweep(x_offset=y_offset, instruction=instruction)
				else:
					return self.horizontal_sweep(x_offset=-y_offset, instruction=instruction)
		self.y += y_offset
		if not self.is_in_field():
			# print("Enter finished.")
			self.num_enters += 1
			return 1
		self.step_on_tile()
		return self.vertical_sweep(y_offset, instruction)

	def horizontal_sweep(self, x_offset, instruction: Instruction):
		if self.is_stuck(x_offset, 0):
			# print("Got stuck.", self.x, self.y)
			return -1
		if not self.is_clear_way(self.x + x_offset, self.y):
			if not self.is_in_field():
				# print("Cant't enter. . .")
				return 1
			if instruction.get_next_strategy() == "right":
				if self.is_clear_way(self.x, self.y + x_offset):
					return self.vertical_sweep(y_offset=x_offset, instruction=instruction)
				else:
					return self.vertical_sweep(y_offset=-x_offset, instruction=instruction)
			else:
				if self.is_clear_way(self.x, self.y - x_offset):
					return self.vertical_sweep(y_offset=-x_offset, instruction=instruction)
				else:
					return self.vertical_sweep(y_offset=x_offset, instruction=instruction)
		self.x += x_offset
		if not self.is_in_field():
			# print("Enter finished.")
			self.num_enters += 1
			return 1
		self.step_on_tile()
		return self.horizontal_sweep(x_offset, instruction)

	def enter_field(self, instruction: Instruction):
		x, y, from_side = instruction.get_starting_coordinates(self.farm)
		self.x = x
		self.y = y
		if from_side == "top":
			self.y -= 1
			return self.vertical_sweep(1, instruction)
		if from_side == "bottom":
			self.y += 1
			return self.vertical_sweep(-1, instruction)
		if from_side == "right":
			self.x += 1
			return self.horizontal_sweep(-1, instruction)
		if from_side == "left":
			self.x -= 1
			return self.horizontal_sweep(1, instruction)

	def paint_map(self, instructions: List[Instruction]):
		for instruction in instructions:
			if self.enter_field(instruction.reset()) == -1:
				return -10
		return 0

	def is_stuck(self, x_offset, y_offset):
		if self.is_clear_way(self.x + x_offset, self.y + y_offset):
			return False
		if x_offset == 0:
			if self.is_clear_way(self.x + 1, self.y) or self.is_clear_way(self.x - 1, self.y):
				return False
		if y_offset == 0:
			if self.is_clear_way(self.x, self.y + 1) or self.is_clear_way(self.x, self.y - 1):
				return False
		return True












