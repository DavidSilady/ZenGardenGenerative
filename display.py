import time
from farm import Farm
import tkinter as tk


class MonkDisplay:
	def __init__(self, canvas, gallery, tile_size):
		self.canvas = canvas
		self.tile_size = tile_size
		self.x = -1
		self.y = -1
		self.image = self.draw(gallery)

	def draw(self, gallery):
		img = gallery.get_img("other_monk" + str(self.tile_size))
		return self.canvas.create_image(self.tile_size / 2, self.tile_size / 2, image=img)

	def move(self, x_offset, y_offset, speed=200):
		speed = 0.05 / speed
		for offset in range(0, self.tile_size):
			time.sleep(speed)
			self.canvas.move(self.image, x_offset, y_offset)
			self.canvas.update()


class Gallery:
	def __init__(self, filenames=None):
		filenames = ["rock", "monk", "other_monk", "sd"]
		self.image_tuples = []
		for filename in filenames:
			try:
				self.image_tuples.append((filename + "75", tk.PhotoImage(file=("gallery/" + filename + "75" + ".png"))))
				self.image_tuples.append((filename + "150", tk.PhotoImage(file=("gallery/" + filename + "150" + ".png"))))
			except tk.TclError:
				print("File " + filename + " not found.")

	def get_img(self, img_name):
		for image_tuple in self.image_tuples:
			if image_tuple[0] == img_name:
				return image_tuple[1]


class Display:
	def __init__(self, farm: Farm, tile_size):
		self.tile_size = tile_size
		width = (farm.width + 2) * tile_size
		height = (farm.height + 2) * tile_size
		root_dimensions = str(width) + "x" + str(height)
		self.root = tk.Tk()
		self.root.geometry(root_dimensions)
		self.canvas = tk.Canvas(self.root, width=width, height=height, bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack(side="top")
		self.canvas.configure(background="#cb9ca1")
		self.gallery = Gallery()
		self.tiles = self.draw_farm(farm)
		self.monk = MonkDisplay(self.canvas, self.gallery, self.tile_size)

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
		# self.color = "#757575"
		self.value = value
		self.x = x
		self.y = y
		self.canvas = canvas
		self.text = None
		self.picture = None
		self.background = None
		if canvas is not None:
			self.draw(canvas, tile_size, gallery)

	def update_color(self):
		self.color = "#cb9ca1"
		self.canvas.itemconfig(self.background, fill=self.color)

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
