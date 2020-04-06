from farm import Farm


class MonkDisplay:
	def __init__(self, canvas, gallery, tile_size):
		self.canvas = canvas
		self.x = -1
		self.y = -1

	def draw(self, gallery, tile_size):
		img = gallery.get_img("other_monk" + str(tile_size))
		self.canvas.create_image(tile_size / 2, tile_size / 2, image=img)


class Monk:
	def __init__(self, farm: Farm, monk_display=None):
		self.monk_display = monk_display
		self.farm = farm
		self.x = 0
		self.y = 0

	def clear_way(self, new_x, new_y):
		"""
		:return: bool if the step is clear (doesn't contain an obstacle)
		"""
		return self.farm.field[new_y][new_x] == -1

	def move_observer(self, x_offset, y_offset):
		for monk in self.monk_display:
			monk.move(x_offset, y_offset)

	def move_up(self):
		new_x = self.x
		new_y = self.y - 1
		if new_y < 0:
			return
		if self.clear_way(new_x, new_y):
			return
		self.y = new_y

	def move_down(self):
		new_x = self.x
		new_y = self.y + 1
		if new_y > self.farm.height:
			return
		if self.clear_way(new_x, new_y):
			return
		self.y = new_y

	def move_right(self):
		new_x = self.x + 1
		new_y = self.y
		if new_x > self.farm.width:
			return
		if self.clear_way(new_x, new_y):
			return
		self.x = new_x

	def move_left(self):
		new_x = self.x - 1
		new_y = self.y
		if new_x < 0:
			return
		if self.clear_way(new_x, new_y):
			return
		self.x = new_x






