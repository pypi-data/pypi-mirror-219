from typing import Tuple

from pulp import LpVariable, LpProblem, LpMinimize, GLPK, value


class Solver:

    def __init__(self):
        self.name = 'UTA GMS Solver'

    def solve(self) -> Tuple[float, float]:
        x = LpVariable("x", 0, 3)
        y = LpVariable("y", 0, 1)
        prob = LpProblem("myProblem", LpMinimize)

        prob += x + y <= 2
        prob += -4 * x + y

        status = prob.solve()
        status = prob.solve(GLPK(msg=0))

        return value(x), value(y)

    def __str__(self):
        return self.name
