import random
from typing import List

from monk import Instruction


def generate_random_indexes(width, height):
	indexes = range(2 * (width + height))
	indexes = [int(i) for i in indexes]
	random.shuffle(indexes)
	return indexes


def generate_random_strategies(num_strategies=3):
	init_array = ["right", "left"] * 3
	random.shuffle(init_array)
	return init_array[:num_strategies]


def assign_strategies(indexes, strategies):
	instructions: List[Instruction] = []
	for starting_point, strategy in indexes, strategies:
		instructions.append(Instruction(starting_point, strategy))
	return instructions




