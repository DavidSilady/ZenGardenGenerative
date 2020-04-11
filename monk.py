from typing import List
from farm import Farm


class Instruction:
	def __init__(self, starting_point, strategies, strategy_index=-1):
		self.starting_point = starting_point
		self.strategies = strategies  # right/left
		self.strategy_index = strategy_index

	def get_starting_coordinates(self, farm):
		start_index = 0
		start_index += self.starting_point
		if start_index < farm.width:  # Top row
			return start_index, 0, "top"
		start_index -= farm.width
		if start_index < farm.height:  # Right column
			return farm.width, start_index, "right"
		start_index -= farm.height
		if start_index < farm.height:  # Left column
			return 0, start_index, "left"
		if start_index < farm.width:  # Bottom row
			return start_index, farm.height, "bottom"
		return -1, -1, "none"

	def get_next_strategy(self):
		self.strategy_index += 1
		return self.strategies[self.strategy_index % len(self.strategies)]


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
		print("Obstacle in the way!")
		return False

	def move_up(self):
		new_x = self.x
		new_y = self.y - 1
		if new_y < 0:
			print("Out of field.")
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
			print("Out of field.")
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
			print("Out of field.")
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
			print("Out of field.")
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
		if not self.is_clear_way(self.x, self.y + y_offset):
			if not self.is_in_field():
				print("Cant't enter. . .")
				return
			if instruction.get_next_strategy() == "right":
				return self.horizontal_sweep(x_offset=-y_offset, instruction=instruction)
			else:
				return self.horizontal_sweep(x_offset=y_offset, instruction=instruction)
		if not self.is_in_field():
			print("Enter finished.")
			self.num_enters += 1
			return
		self.step_on_tile()
		self.y += y_offset
		self.vertical_sweep(y_offset, instruction)

	def horizontal_sweep(self, x_offset, instruction: Instruction):
		if not self.is_clear_way(self.x + x_offset, self.y):
			if not self.is_in_field():
				print("Cant't enter. . .")
				return
			if instruction.get_next_strategy() == "right":
				return self.vertical_sweep(y_offset=x_offset, instruction=instruction)
			else:
				return self.vertical_sweep(y_offset=-x_offset, instruction=instruction)
		if not self.is_in_field():
			print("Enter finished.")
			self.num_enters += 1
			return
		self.step_on_tile()
		self.x += x_offset
		self.horizontal_sweep(x_offset, instruction)

	def enter_field(self, instruction: Instruction):
		x, y, from_side = instruction.get_starting_coordinates(self.farm)
		self.x = x
		self.y = y
		if from_side == "top":
			self.vertical_sweep(1, instruction)
		if from_side == "bottom":
			self.vertical_sweep(-1, instruction)
		if from_side == "right":
			self.horizontal_sweep(-1, instruction)
		if from_side == "left":
			self.horizontal_sweep(1, instruction)

	def paint_map(self, instructions: List[Instruction]):
		for instruction in instructions:
			self.enter_field(instruction)









