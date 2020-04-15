import random
from copy import deepcopy
from math import floor
from typing import List

from monk import Instruction, Monk


def generate_random_indexes(width, height):
	indexes = range(2 * (width + height))
	indexes = [int(i) for i in indexes]
	random.shuffle(indexes)
	return indexes


def generate_random_strategy(num_turns=3):
	init_strategy = ["right", "left"] * num_turns
	random.shuffle(init_strategy)
	return init_strategy[:num_turns]


def generate_random_instructions(width, height):
	"""
	creates instruction array, effectively assigning random indexes to random strategies
	:return: Instruction array
	"""
	indexes = generate_random_indexes(width, height)
	instructions: List[Instruction] = []
	for starting_point in indexes:
		instructions.append(Instruction(starting_point, generate_random_strategy()))
	return instructions


class Subject:
	def __init__(self, farm, mother=None, father=None):
		self.monk = Monk(deepcopy(farm))
		self.fitness = 0
		if mother is None and father is None:
			self.instructions: List[Instruction] = generate_random_instructions(farm.width,
			                                                                    farm.height)
		else:
			self.instructions: List[Instruction] = frick(mother, father)

	def print_instructions(self):
		for instruction in self.instructions:
			instruction.print_instruction(self.monk.farm)

	def calculate_fitness(self):
		self.monk.farm.clear()
		self.monk.paint_map(self.instructions)
		self.fitness = self.monk.farm.count_fitness()
		return self.fitness


def frick(mother: Subject, father: Subject):
	combination_length = floor(len(mother.instructions)/4)
	instructions: List[Instruction] = mother.instructions[:combination_length]
	instructions += father.instructions[combination_length:combination_length*2]
	instructions += mother.instructions[combination_length*2:combination_length*3]
	instructions += father.instructions[combination_length*3:]
	return instructions

