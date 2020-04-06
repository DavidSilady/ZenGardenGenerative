from farm import Farm


class Monk:
	def __init__(self, farm: Farm):
		self.farm = farm
		self.x = -1
		self.y = -1

	def step_on_tile(self, x, y):
		self.farm.field[y][x] = 1

	def clear_way(self, new_x, new_y):
		"""
		:return: bool if the step is clear (doesn't contain an obstacle)
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
			self.y = new_y
			return 0, -1
		if not self.clear_way(new_x, new_y):
			return 0, 0
		self.y = new_y
		return 0, -1

	def move_down(self):
		new_x = self.x
		new_y = self.y + 1
		if new_y >= self.farm.height:
			print("Out of field.")
			if new_y >= self.farm.height + 1:
				return 0, 0
			self.y = new_y
			return 0, 1
		if not self.clear_way(new_x, new_y):
			return 0, 0
		self.y = new_y
		return 0, 1

	def move_right(self):
		new_x = self.x + 1
		new_y = self.y
		if new_x >= self.farm.width:
			print("Out of field.")
			if new_x >= self.farm.width + 1:
				return 0, 0
			self.x = new_x
			return 1, 0
		if not self.clear_way(new_x, new_y):
			return 0, 0
		self.x = new_x
		return 1, 0

	def move_left(self):
		new_x = self.x - 1
		new_y = self.y
		if new_x < 0:
			print("Out of field.")
			if new_x < -1:
				return 0, 0
			self.x = new_x
			return -1, 0
		if not self.clear_way(new_x, new_y):
			return 0, 0
		self.x = new_x
		return -1, 0






