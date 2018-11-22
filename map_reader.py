import os
import re
import numpy as np
from utils import TERMINAL_STATES
from state import State


class NPuzzlesMap:

    MIN_SHAPE = (3, 3)

    def __init__(self, shape: tuple, initial_map: np.ndarray, notation='snail'):
        if shape < self.MIN_SHAPE:
            raise self.BadMapError()
        self.initial_map = initial_map
        self.initial_state = State(self.initial_map)
        dimension, _ = shape

        # notation_dict = TERMINAL_STATES.get(notation)

        terminal_array = TERMINAL_STATES.get(dimension)
        self.terminal_state = State(terminal_array)

    @staticmethod
    def __map_from_file(filename: str) -> np.ndarray:
        dimension = None
        start_map = []
        if not os.path.isfile(filename):
            raise Exception(f'File {filename} does not exist')
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if dimension is None and re.fullmatch(r'\d+', line):
                    dimension = int(line)
                elif dimension is not None:
                    row = re.findall(r'\d+', line)
                    row = [int(digit) for digit in row[:dimension]]
                    start_map.append(row)
        return np.array(start_map)

    @staticmethod
    def __map_from_string(string_map: str) -> np.ndarray:
        dimension = None
        start_map = list()
        lines = string_map.split('\n')
        lines.pop(-1)
        for line in lines:
            line.strip()
            if dimension is None and re.fullmatch(r'\d+', line):
                dimension = int(line)
            elif dimension is not None:
                row = re.findall(r'\d+', line)
                row = [int(digit) for digit in row[:dimension]]
                start_map.append(row)
        return np.array(start_map)

    @classmethod
    def from_file(cls, filename):
        initial_map = cls.__map_from_file(filename)
        return cls(initial_map.shape, initial_map)

    @classmethod
    def from_string(cls, string_map):
        initial_map = cls.__map_from_string(string_map)
        return cls(initial_map.shape, initial_map)

    class BadMapError(Exception):
        def __init__(self, message='Bad map', error=None):
            super().__init__(message)
            self.error = error

    def __str__(self):
        return f'Initial{self.initial_state}, Terminal{self.terminal_state}'

    def __repr__(self):
        return self.__str__()
