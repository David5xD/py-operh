import numpy as np
from pyoperh.transportation_problem.transportation_problem import TransportationProblem


class VogelsApproximation(TransportationProblem):
    def __init__(self, demand, supply, sources, destinations, routes):
        TransportationProblem.__init__(self, demand, supply, sources, destinations, routes)

    def get_min_cost_cell(self):
        '''Find the coordinates of the cell with minimum cost'''
        return np.unravel_index(self.routes.argmin(), self.routes.shape)

    def get_penalty_index(self, row_difference, col_difference):
        '''Finds penalty and returns its route'''
        size = len(row_difference)
        difference = row_difference + col_difference
        max_diff = max(difference)
        index = difference.index(max_diff)
        if index >= size:
            index -= size
            return self.routes[:, index].argmin(), index
        else:
            return index, self.routes[index].argmin()

    def get_difference_values(self):
        '''Returns row and column differences'''
        row_routes = np.copy(self.routes)
        row_difference = []
        num_rows = self.routes.shape[0]
        col_routes = np.copy(self.routes)
        col_difference = []
        num_cols = self.routes.shape[1]
        if num_cols > 1:
            for i in range(0, num_rows):
                row_routes = row_routes[:, row_routes[i].argsort(kind='mergesort')]
                row_difference.append(row_routes[i][1] - row_routes[i][0])
        if num_rows > 1:
            for i in range(0, num_cols):
                col_routes = col_routes[col_routes[:, i].argsort(kind='mergesort')]
                col_difference.append(col_routes[1][i] - col_routes[0][i])
        return row_difference, col_difference

    def main(self):
        '''Implements Vogel's Approximation Method'''
        while self.routes.size > 0:
            # Directly calculate minimum index if there is only one row or column left
            if self.routes.shape[0] == 1 or self.routes.shape[1] == 1:
                i, j = self.get_min_cost_cell()
            else:
                row_diff, col_diff = self.get_difference_values()
                i, j = self.get_penalty_index(row_diff, col_diff)
            cost = self.routes[i][j]
            # Determine the max amount of goods that can be transported through this route
            goods = min(self.supply[i], self.demand[j])
            self.supply[i] -= goods
            self.demand[j] -= goods
            self.solution.append({"source": self.sources[i], "destination": self.destinations[j], "cost": cost, "goods": goods})
            self.reset_routes(i, j)
