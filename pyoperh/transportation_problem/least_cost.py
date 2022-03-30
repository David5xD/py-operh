import numpy as np
from pyoperh.transportation_problem.transportation_problem import TransportationProblem


class LeastCost(TransportationProblem):
    def __init__(self, demand, supply, sources, destinations, routes):
        TransportationProblem.__init__(self, demand, supply, sources, destinations, routes)

    def get_min_cost_cell(self):
        '''Find the coordinates of the cell with minimum cost'''
        return np.unravel_index(self.routes.argmin(), self.routes.shape)

    def main(self):
        '''Implementation of Least Cost method'''
        while self.routes.size > 0:
            # Get coordinates of minimum valued cell in the self.routes
            i, j = self.get_min_cost_cell()
            cost = self.routes[i][j]
            # Determine the max amount of goods that can be transported through this route
            goods = min(self.supply[i], self.demand[j])
            self.supply[i] -= goods
            self.demand[j] -= goods
            self.solution.append({"source": self.sources[i], "destination": self.destinations[j], "cost": cost, "goods": goods})
            self.reset_routes(i, j)
