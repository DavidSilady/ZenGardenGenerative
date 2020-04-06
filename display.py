import time
from farm import Farm
import tkinter as tk

from monk import Monk


class MonkDisplay:
	def __init__(self, canvas, root, gallery, tile_size, logic_monk: Monk):
		self.logic_monk = logic_monk
		self.canvas = canvas
		self.tile_size = tile_size
		self.image = self.draw(gallery)

	def draw(self, gallery):
		img = gallery.get_img("other_monk" + str(self.tile_size))
		return self.canvas.create_image(self.tile_size / 2, self.tile_size / 2, image=img)

	def move(self, x_offset, y_offset, speed=200):
		print(self.logic_monk.x, self.logic_monk.y)
		speed = 0.05 / speed
		for offset in range(0, self.tile_size):
			time.sleep(speed)
			self.canvas.move(self.image, x_offset, y_offset)
			self.canvas.update()


class Gallery:
	def __init__(self, filenames=None):
		if filenames is None:
			filenames = ["rock", "monk", "other_monk", "dirt"]
		self.image_tuples = []
		for filename in filenames:
			try:
				self.image_tuples.append((filename + "75", tk.PhotoImage(file=("gallery/" + filename + "75" + ".png"))))
				self.image_tuples.append(
					(filename + "150", tk.PhotoImage(file=("gallery/" + filename + "150" + ".png"))))
			except tk.TclError:
				print("File " + filename + " not found.")

	def get_img(self, img_name):
		for image_tuple in self.image_tuples:
			if image_tuple[0] == img_name:
				return image_tuple[1]


class Display:
	def __init__(self, farm: Farm, tile_size, monk):
		self.tile_size = tile_size
		width = (farm.width + 2) * tile_size
		height = (farm.height + 2) * tile_size
		root_dimensions = str(width) + "x" + str(height)
		self.farm = farm
		self.root = tk.Tk()
		self.root.geometry(root_dimensions)
		self.canvas = tk.Canvas(self.root, width=width, height=height, bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack(side="top")
		self.canvas.configure(background="#cb9ca1")
		self.gallery = Gallery()
		self.tiles = self.draw_farm(farm)
		self.display_monk = MonkDisplay(self.canvas, self.root, self.gallery, self.tile_size, monk)
		self.move_enabled = True
		self.root.bind("<Key>", self.on_keypress)

	def on_keypress(self, event):
		if not self.move_enabled:
			return
		self.move_enabled = False
		x = 0
		y = 0
		print(event.char)
		if event.char == "w":
			x, y = self.display_monk.logic_monk.move_up()
		if event.char == "a":
			x, y = self.display_monk.logic_monk.move_left()
		if event.char == "s":
			x, y = self.display_monk.logic_monk.move_down()
		if event.char == "d":
			x, y = self.display_monk.logic_monk.move_right()
		self.display_monk.move(x, y)
		self.move_enabled = True
		if self.display_monk.logic_monk.is_in_field():
			x = self.display_monk.logic_monk.x
			y = self.display_monk.logic_monk.y
			self.tiles[y][x].update_color(self.farm.field[y][x], self.gallery, self.tile_size)

	def run(self):
		self.root.mainloop()

	def draw_farm(self, farm: Farm):
		tiles = [[Tile(0, 0, -1, -1) for x in range(farm.width)] for y in range(farm.height)]
		for y in range(farm.height):
			for x in range(farm.width):
				tile = Tile(farm.field[y][x], self.tile_size, x + 1, y + 1, self.canvas, self.gallery)
				tiles[y][x] = tile
		return tiles


class Tile:
	def __init__(self, value, tile_size, x, y, canvas=None, gallery=None):
		self.color = "#ffcdd2"
		# if value == -1:
		# 	self.color = "#ffcdd2"
		self.value = value
		self.x = x
		self.y = y
		self.canvas = canvas
		self.text = None
		self.picture = None
		self.background = None
		if canvas is not None:
			self.draw(canvas, tile_size, gallery)

	def update_color(self, number, gallery, tile_size):
		# self.color = "#cb9ca1"
		self.canvas.itemconfig(self.background, fill=self.color)
		self.canvas.itemconfig(self.text, text=int(number))
		self.canvas.delete(self.picture)

	def draw(self, canvas, tile_size, gallery: Gallery):
		canvas_x = int(self.x * tile_size)
		canvas_y = int(self.y * tile_size)
		self.background = canvas.create_rectangle(canvas_x, canvas_y, canvas_x + tile_size, canvas_y + tile_size,
		                                          fill=self.color,
		                                          width=0)
		center_x = canvas_x + (tile_size / 2)
		center_y = canvas_y + (tile_size / 2)

		self.text = canvas.create_text(center_x, center_y, text=str(self.value), fill="white", font=str(tile_size * 2))

		if self.value == -1:
			img = gallery.get_img("rock" + str(tile_size))
			self.picture = canvas.create_image(center_x, center_y, image=img)
		else:
			img = gallery.get_img("dirt" + str(tile_size))
			self.picture = canvas.create_image(center_x, center_y, image=img)


