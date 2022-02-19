#!/usr/bin/env python3
# this script has a tendency to freeze, because of line 33
# if that happens, just restart it
import math
import random
import itertools
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import elementary_functions

Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko'),
    trim_blocks=True,
    lstrip_blocks=True)

def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def main():
    # add limits that will require sandwich theorem to figure out
    # notice how all these functiosn have an upper/lower bound
    top_functions_space = [sympy.sin('x'), sympy.cos('x'), sympy.sympify('cos(x!)'), sympy.sympify('arctan(x)')]
    top_functions = elementary_functions.elementary_function_generator(2, functions_space=top_functions_space)
    # notice how all these functions -> oo as x -> oo
    bottom_functions = [sympy.sympify('2**x'), sympy.sympify('x**x'), sympy.sympify('x**3 + 2'), sympy.sympify('x!')]
    problems = ((top_function / bottom_function) for top_function, bottom_function in elementary_functions.random_product(top_functions, bottom_functions))
    # sympy can't compute some of the limits
    problems = take(filter(lambda x: x.limit('x', math.inf).is_number, problems), 10)

    nth_root_problems = [sympy.sympify('3**x'), sympy.sympify('pi**x'), sympy.sympify('7**x'), sympy.sympify('(2/3)**x')]
    nth_root = sympy.sympify('y**(1/x)')
    nth_root_problems = map(sum, itertools.combinations(nth_root_problems, 3))
    problems += (nth_root.subs('y', problem) for problem in nth_root_problems)

    # add limit problems
    polynomial_generator = elementary_functions.polynomial_generator(count=10, min_order=2, max_order=4)
    polynomial_generator1 = elementary_functions.polynomial_generator(count=10, min_order=3, max_order=4)
    problems += [(top_function / bottom_function) for top_function, bottom_function in zip(polynomial_generator, polynomial_generator1)]

    # shuffle for variety
    random.shuffle(problems)

    # calculate the limits and then convert into LaTeX
    awnsers = (sympy.printing.latex(function.limit('x', math.inf)) for function in problems)
    # we usually use `n` instead of `x` when doing limits
    problems = (problem.subs('x', 'n') for problem in problems)
    # generate LaTeX code for problem statments
    problems = (sympy.printing.latex(problem) for problem in problems)

    # output the LaTeX code
    latex = ENV \
            .get_template('limits_worksheet.jinja.tex') \
            .render(tasks=[Task('Find $\\lim\\limits_{n \\to \\infty} a_{n}$ when:', problems, awnsers)])
    print(latex)

if __name__ == '__main__':
    main()

