from pyoperh.transportation_problem.transportation_problem import TransportationProblem


class NorthWestCorner(TransportationProblem):
    def __init__(self, demand, supply, sources, destinations, routes):
        TransportationProblem.__init__(self, demand, supply, sources, destinations, routes)

    def main(self):
        '''Implementation of Least Cost method'''
        while self.routes.size > 0:
            # Get coordinates of the northwest corner from the routes matrix
            i, j = (0, 0)
            cost = self.routes[i][j]
            # Determine the max amount of goods that can be transported through this route
            goods = min(self.supply[i], self.demand[j])
            self.supply[i] -= goods
            self.demand[j] -= goods
            self.solution.append({"source": self.sources[i], "destination": self.destinations[j], "cost": cost, "goods": goods})
            self.reset_routes(i, j)
