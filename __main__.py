#!/usr/bin/env python3
import sympy

import zadanko.quadratics
import zadanko.elementary_functions as elementary_functions

from jinja2 import Environment, PackageLoader

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def main1():
    zero_solutions_quadratics = [zadanko.quadratics.generate_quadratic_zero_solutions() for i in range(10)]
    one_solution_quadratics = [zadanko.quadratics.generate_quadratic_one_solution() for i in range(10)]
    two_solutions_quadratics = [zadanko.quadratics.generate_quadratic_two_solutions() for i in range(6)]
    zero_solutions_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)
    one_solution_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)
    two_solutions_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)

    problem_list = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    random_quadratics = []
    for i in range(len(zero_solutions_quadratics) + len(one_solution_quadratics) + len(two_solutions_quadratics)):
        choice = random.choice(problem_list)
        random_quadratics.append(choice.pop())
        if not choice:
            problem_list.remove(choice)

    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in random_quadratics)
    random_quadratics = map(sympy.printing.latex, sorted(random_quadratics, key=zadanko.quadratics.quadratic_difficulty_comperator))

    latex = ENV.get_template('problems.jinja.tex').render(equations=random_quadratics, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

def main():
    random_functions = [elementary_functions.generate_elementary_function() for i in range(26)]
    random_functions.sort(key=sympy.count_ops)
    awnsers = (sympy.printing.latex(function.diff()) for function in random_functions)
    random_functions = map(sympy.printing.latex, random_functions)

    latex = ENV.get_template('diffrentiation_problems.jinja.tex').render(equations=random_functions, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

if __name__ == '__main__':
    main()
