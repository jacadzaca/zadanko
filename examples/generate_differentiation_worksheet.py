#!/usr/bin/env python3
''' Generate a worksheet that contains problems on differentiation '''
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

def generate_differentiation_task():
    # generate 10 elementary functions that are made out of 2 composite functions and append them to the problem list
    differentiation_problems = take(elementary_functions.elementary_function_generator(2), 10)
    # generate 10 elementary functions that are at most made out of 2 composite functions and then append the multiplication of them to the problem list
    for function, function1 in zip(take(elementary_functions.elementary_function_generator(2), 10), take(elementary_functions.elementary_function_generator(2), 10)):
        differentiation_problems.append(function * function1)
    # generate 6 elementary functions that are madeout of 3 composite functions and append them to the problem list
    differentiation_problems += take(elementary_functions.elementary_function_generator(3), 6)
    # sort them by how 'complicated' they are - the more 'composite', the later it's in the list
    differentiation_problems.sort(key=sympy.count_ops)
    # differentiate and generate LaTeX code
    awnsers = (sympy.printing.latex(function.diff()) for function in differentiation_problems)
    # generate LaTeX code for problem statments
    differentiation_problems = map(sympy.printing.latex, differentiation_problems)
    return Task('Find the derivative of function $f$, given by expression:', differentiation_problems, awnsers)

if __name__ == '__main__':
    # output the LaTeX code
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_differentiation_task()])
    print(latex)

