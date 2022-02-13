#!/usr/bin/env python3
import math
import sympy
import string
import random

from sympy.abc import x
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader

ENV = Environment(
    loader=FileSystemLoader('zadanko/templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def main1():
    random_quadratics = [generate_random_quadratic() for i in range(26)]
    awnsers = (sympy.printing.latex(sympy.solvers.solveset(quadratic, domain=sympy.S.Reals)) for quadratic in random_quadratics)
    random_quadratics = map(sympy.printing.latex, random_quadratics)

    latex = ENV.get_template('problems.jinja.tex').render(equations=random_quadratics, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

def main():
    random_functions = [generate_elementary_function() for i in range(26)]
    awnsers = (sympy.printing.latex(function.diff()) for function in random_functions)
    random_functions = map(sympy.printing.latex, random_functions)

    latex = ENV.get_template('diffrentiation_problems.jinja.tex').render(equations=random_functions, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

def generate_elementary_function():
    elementary_functions = [sympy.sin('x'), sympy.cos('x'), sympy.tan('x'), sympy.asin('x'), sympy.acos('x'), sympy.atan('x'), sympy.ln('x'), sympy.exp('x'), generate_random_polynomial()]
    with sympy.evaluate(False):
        return random.choice(elementary_functions).subs('x', random.choice(elementary_functions))

def generate_random_polynomial(max_order=4):
    order = random.randint(2, max_order)
    polynomial = ''
    for i in range(order, -1, -1):
        cofficient = random.randint(1, 10)
        polynomial += f' + {cofficient}*x**{i}'
    return sympy.sympify(polynomial)

def generate_random_quadratic():
    b = random.randint(math.ceil(math.sqrt(8)), 17)
    a = random.randint(1, (b**2)//8)
    c = random.randint(1, (b**2)//(4*a))
    return sympy.sympify(f'{a}*x**2 + {b}*x + {c}')

if __name__ == '__main__':
    main()
