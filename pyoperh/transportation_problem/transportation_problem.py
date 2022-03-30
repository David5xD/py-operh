import numpy as np
from tabulate import tabulate


class TransportationProblem:
    def __init__(self, demand, supply, sources, destinations, routes):
        self.demand = demand
        self.supply = supply
        self.sources = sources
        self.destinations = destinations
        self.routes = routes
        self.solution = []
        self.balance_problem()
        print(self.demand, self.supply)

    def balance_problem(self):
        '''Balances the given transportation problem in case it is unbalanced'''
        balance = sum(self.supply) - sum(self.demand)
        if balance > 0:
            self.destinations = np.append(self.destinations, "*")
            self.demand = np.append(self.demand, balance)
            balance_column = np.zeros(self.routes.shape[0])
            self.routes = np.column_stack((self.routes, balance_column))
        elif balance < 0:
            balance *= -1
            self.supply = np.append(self.supply, "*")
            self.supply = np.append(self.supply, balance)
            balance_row = np.zeros(self.routes.shape[1])
            self.routes = np.vstack((self.routes, balance_row))

    def reset_routes(self, x, y):
        '''Discard routes for which the defined supply or demand has been fulfilled'''
        if self.supply[x] == 0:
            # Discard source if supply is depleted
            self.supply = np.delete(self.supply, x)
            self.sources = np.delete(self.sources, x)
            self.routes = np.delete(self.routes, x, 0)
        if self.demand[y] == 0:
            # Discard destination if demand has been fulfilled
            self.demand = np.delete(self.demand, y)
            self.destinations = np.delete(self.destinations, y)
            self.routes = np.delete(self.routes, y, 1)

    def calc_basic_solution(self):
        '''Calculates the basic solution of the given transportation problem'''
        basic_solution = 0
        for route in self.solution:
            basic_solution += route["cost"] * route["goods"]
        return basic_solution

    def main(self):
        '''Implements the main logic to solve the transporatation problem'''
        pass

    def print_output(self):
        '''Prints the solution of the problem in a tabular form'''
        self.main()
        basic_solution = self.calc_basic_solution()
        solution_list = []
        for sol in self.solution:
            if sol["source"] == '*' or sol["destination"] == '*':
                continue
            solution_list.append([sol["source"], sol["destination"], sol["goods"], sol["cost"], sol["cost"] * sol["goods"]])
        print(tabulate(solution_list, headers=["Source", "Destination", "Goods", "Route Cost", "Total Cost"], tablefmt='github'))
        print(f"\nBasic Solution: {basic_solution}")
