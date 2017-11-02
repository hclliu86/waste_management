# -*- coding: UTF-8 -*-
# __author__ = 'liuhc'
import collections
from random import uniform
from datetime import datetime


id_formation = "%y%m%d%H%M%S"
pellets_storage_capacity = 32
combination_height_limitation = 750
uniform_distribute_upper_bound = 300
uniform_distribute_lower_bound = 150

refill_batches = 100
total_number_of_pellets_for_testing = 1400


class PelletsOptimization:
    def __init__(self):
        self.UnsortedPellets = []
        self.SortedPellets = []
        self.StorageCapacity = pellets_storage_capacity
        self.total_pellets_refilled = total_number_of_pellets_for_testing
        self.total_pellets_optimized = total_number_of_pellets_for_testing

    def refill_pellets(self):
        remain_capacity = self.StorageCapacity - len(self.UnsortedPellets)
        for i in range(min(remain_capacity, self.total_pellets_refilled)):
            id_of_pellet = datetime.now().strftime(id_formation) + str(i)
            waste_type = 'DAW'
            height = uniform(uniform_distribute_lower_bound, uniform_distribute_upper_bound)
            self.UnsortedPellets.append(Pellet(ID=id_of_pellet, waste_type=waste_type, height=height))
            self.total_pellets_refilled -= 1

    def knapsack_optimize(self):
        self.UnsortedPellets.sort(key=lambda x: x.height, reverse=True)
        while len(self.UnsortedPellets) > 3:
            current_combination = []
            height_limitation = combination_height_limitation
            for unsorted_pellet in self.UnsortedPellets:
                if unsorted_pellet.height < height_limitation:
                    current_combination.append(unsorted_pellet)
                    height_limitation -= unsorted_pellet.height
            self.SortedPellets.append(current_combination)
            for sorted_pellet in current_combination:
                # print(sorted_pellet)
                # print(self.total_pellets_optimized)
                self.UnsortedPellets.remove(sorted_pellet)
                self.total_pellets_optimized -= 1

    def random_guess(self):
        while len(self.UnsortedPellets) >= 2:
            current_combination = [self.UnsortedPellets.pop(0)]
            self.total_pellets_optimized -= 1
            current_height = current_combination[0].height
            while current_height < combination_height_limitation and len(self.UnsortedPellets) > 0:
                if current_height + self.UnsortedPellets[0].height <= combination_height_limitation:
                    current_combination.append(self.UnsortedPellets.pop(0))
                    current_height += current_combination[-1].height
                    self.total_pellets_optimized -= 1
                else:
                    self.SortedPellets.append(current_combination)
                    break

    def average_combin(self):
        self.UnsortedPellets.sort(key=lambda x: x.height, reverse=True)
        while len(self.UnsortedPellets) > 3:
            current_combination = []
            height_limitation = combination_height_limitation
            number_of_unsorted_pellets = len(self.UnsortedPellets)
            current_combination.append()

    def start_optimization(self, test_with_total_pellet_number=True):
        if test_with_total_pellet_number:
            while self.total_pellets_refilled > 0:
                self.refill_pellets()
                # self.random_guess()
                self.knapsack_optimize()
            # print(len(self.SortedPellets), ' combinations generated!')


Pellet = collections.namedtuple('Pellet', ['ID', 'waste_type', 'height'])


if __name__ == '__main__':
    tests = 100
    total_combinations = 0
    pellets_filled_to_200L_drum = 0
    for test in range(tests):
        opt = PelletsOptimization()
        opt.start_optimization()
        total_combinations += len(opt.SortedPellets)
        pellets_filled_to_200L_drum += total_number_of_pellets_for_testing - opt.total_pellets_optimized
    print('The mean of combinations: ', total_combinations / tests)
    print('The mean of pellet being filled: ', pellets_filled_to_200L_drum / tests)
    print('The mean capacity of 200L drum: {:.2f}'.format(pellets_filled_to_200L_drum / total_combinations))