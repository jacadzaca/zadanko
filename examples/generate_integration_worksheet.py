#!/usr/bin/env python3
''' Generate a worksheet that contains problems on integration'''
import collections
import itertools

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import elementary_functions

Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko'),
    trim_blocks=True,
    lstrip_blocks=True)

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def generate_integration_task():
    # generate awnsers first - it's easier to ensure the problems will be integrable that way
    awnsers = take(filter(lambda expr: expr.diff() != 1, elementary_functions.elementary_function_generator(2)), 16)
    random_functions = itertools.cycle(elementary_functions.elementary_function_generator(1))
    awnsers += ((left_func * right_func) for left_func, right_func in zip(take(random_functions, 10), take(random_functions, 10)))
    awnsers.sort(key=sympy.count_ops)
    # generate problems
    problems = (sympy.printing.latex(function.diff()) for function in awnsers)
    awnsers = map(sympy.printing.latex, awnsers)

    return Task('Integrate function $f$, given by expression:', problems, awnsers)

if __name__ == '__main__':
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_integration_task()])
    print(latex)

