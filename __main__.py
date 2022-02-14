#!/usr/bin/env python3
import itertools

import sympy

import zadanko.elementary_functions as elementary_functions

from jinja2 import Environment, PackageLoader

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def main():
    random_functions = take(elementary_functions.elementary_function_generator(2), 10)
    for function, function1 in zip(take(elementary_functions.elementary_function_generator(2), 10), take(elementary_functions.elementary_function_generator(2), 10)):
        random_functions.append(function * function1)
    random_functions += take(elementary_functions.elementary_function_generator(3), 6)
    random_functions.sort(key=sympy.count_ops)
    awnsers = (sympy.printing.latex(function.diff()) for function in random_functions)
    random_functions = map(sympy.printing.latex, random_functions)

    latex = ENV.get_template('diffrentiation_problems.jinja.tex').render(equations=random_functions, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

if __name__ == '__main__':
    main()
