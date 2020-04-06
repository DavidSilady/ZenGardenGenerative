from farm import Farm


class Monk:
	def __init__(self, farm: Farm, display=None):
		self.display = display
		self.farm = farm
		self.x = 0
		self.y = 0

	def step_on_tile(self, x, y):
		self.farm.field[y][x] = 1

	def clear_way(self, new_x, new_y):
		"""
		:return: bool if the step is clear (doesn't contain an obstacle)
		"""
		return self.farm.field[new_y][new_x] == -1

	def display_move(self, x_offset, y_offset):
		for root in self.display:
			root.monk.move(x_offset, y_offset)

	def move_up(self):
		new_x = self.x
		new_y = self.y - 1
		if new_y < 0:
			return
		if self.clear_way(new_x, new_y):
			return
		self.y = new_y
		self.display_move(0, -1)

	def move_down(self):
		new_x = self.x
		new_y = self.y + 1
		if new_y > self.farm.height:
			return
		if self.clear_way(new_x, new_y):
			return
		self.y = new_y
		self.display_move(0, 1)

	def move_right(self):
		new_x = self.x + 1
		new_y = self.y
		if new_x > self.farm.width:
			return
		if self.clear_way(new_x, new_y):
			return
		self.x = new_x
		self.display_move(1, 0)

	def move_left(self):
		new_x = self.x - 1
		new_y = self.y
		if new_x < 0:
			return
		if self.clear_way(new_x, new_y):
			return
		self.x = new_x
		self.display_move(-1, 0)






