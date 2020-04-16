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
		self.monk = Monk(farm)
		self.fitness = 0
		if mother is None and father is None:
			self.instructions: List[Instruction] = generate_random_instructions(farm.width,
			                                                                    farm.height)
		else:
			self.instructions: List[Instruction] = frick(mother, father)

	def __repr__(self):
		return repr(self.fitness)

	def print_instructions(self):
		for instruction in self.instructions:
			instruction.print_instruction(self.monk.farm)

	def calculate_fitness(self):
		self.monk.farm.clear()
		penalty = self.monk.paint_map(self.instructions)
		self.fitness = self.monk.farm.count_fitness() + penalty
		return self.fitness

	def mutate_strategy(self):
		self.instructions[random.randint(0, len(self.instructions) - 1)].strategy = generate_random_strategy()

	def mutate_entry(self):
		num_points = (self.monk.farm.height + self.monk.farm.width) * 2
		self.instructions[random.randint(0, len(self.instructions) - 1)].starting_point = random.randint(0, num_points - 1)


def frick(mother: Subject, father: Subject):
	combination_length = floor(len(mother.instructions) / 4)
	instructions: List[Instruction] = mother.instructions[:combination_length]
	instructions += father.instructions[combination_length:combination_length * 2]
	instructions += mother.instructions[combination_length * 2:combination_length * 3]
	instructions += father.instructions[combination_length * 3:]
	return instructions


class Generation:
	def __init__(self, farm, prev_generation=None):
		self.subjects: List[Subject] = []
		self.average_fitness = 0
		self.farm = farm
		if prev_generation is None:
			self.subjects = generate_new_subjects(farm)
		else:
			self.new_subjects(prev_generation)
		self.mutate()
		self.calculate_average_fitness()

	def new_subjects(self, prev_generation):
		preserved_subjects: List[Subject] = tournament(prev_generation)
		self.subjects = preserved_subjects + self.generation_crossover(preserved_subjects)
		self.subjects.append(prev_generation.get_best_subject())
		self.subjects += generate_new_subjects(self.farm, len(prev_generation.subjects) - len(self.subjects))

	def generation_crossover(self, parents):
		children: List[Subject] = []
		for mother in parents:
			for father in parents:
				if not father == mother:
					children.append(Subject(self.farm, mother, father))
		return children

	def calculate_average_fitness(self):
		total = 0
		for sub in self.subjects:
			total += sub.calculate_fitness()
		self.average_fitness = total / len(self.subjects)
		return self.average_fitness

	def print_all_fitness(self):
		output = ""
		subjects = sorted(self.subjects, key=lambda subject: subject.fitness, reverse=True)
		for sub in subjects:
			output += " " + str(sub.fitness)
		print(output)

	def get_best_subject(self):
		best_subject = sorted(self.subjects, key=lambda subject: subject.fitness, reverse=True)[0]
		return best_subject

	def mutate(self, probability=0.1):
		num_mutated = floor(len(self.subjects) * probability)
		random.shuffle(self.subjects)
		for subject in self.subjects[:num_mutated]:
			subject.mutate_strategy()
		random.shuffle(self.subjects)
		for subject in self.subjects[:num_mutated]:
			subject.mutate_entry()


def tournament(generation: Generation, probability=0.2):
	num_to_preserve = floor(len(generation.subjects) * probability)
	random.shuffle(generation.subjects)
	preserved_subjects = generation.subjects[:num_to_preserve * 2]
	return sorted(preserved_subjects,
	              key=lambda subject:
	              subject.fitness, reverse=True)[:num_to_preserve]


def generate_new_subjects(farm, num_subjects=50):
	subjects: List[Subject] = []
	for _ in range(num_subjects):
		subjects.append(Subject(farm))
	return subjects
