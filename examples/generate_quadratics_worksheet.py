#!/usr/bin/env python3
''' Generate a worksheet that contains problems on quadratics '''
import random
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import quadratics

Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko'),
    trim_blocks=True,
    lstrip_blocks=True)

def generate_quadratics_task():
    # generate diffrent kinds of quadratic equations
    zero_solutions_quadratics = [quadratics.generate_quadratic_zero_solutions() for _ in range(10)]
    one_solution_quadratics = [quadratics.generate_quadratic_one_solution() for _ in range(10)]
    two_solutions_quadratics = [quadratics.generate_quadratic_two_solutions() for _ in range(6)]
    # sort them according to 'difficulty' - the greater the sum of quadratic's coefficients, the more difficult it is
    zero_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    one_solution_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    two_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)

    # arrange the problems in random order, but try to keep the problem's difficulty incremental
    problems = []
    problem_lists = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    for _ in range(sum(map(len, problem_lists))):
        choice = random.choice(problem_lists)
        problems.append(choice.pop())
        if not choice:
            problem_lists.remove(choice)

    # generate the awnsers with sympy https://docs.sympy.org/latest/index.html
    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in problems)
    # generate LaTeX code
    problems = map(sympy.printing.latex, problems)
    return Task('Find the roots of function $f$, given by expression:', problems, awnsers)

if __name__ == '__main__':
    #output latex code
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_quadratics_task()])
    print(latex)

