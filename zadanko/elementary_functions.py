import itertools

import sympy
import random

from zadanko import SIGN

ID = sympy.sympify('x')

ELEMENTARY_FUNCTIONS = [
        sympy.sin('x'),
        sympy.cos('x'),
        sympy.tan('x'),
        sympy.asin('x'),
        sympy.acos('x'),
        sympy.atan('x'),
        sympy.ln('x'),
        sympy.exp('x'),
        sympy.sympify('x**(1/2)'),
        sympy.sympify('x**(2/3)'),
        sympy.sympify('x**(3/2)'),
        sympy.sympify('1/x'),
]

def compose(iterable):
    composition = ID
    for function in iterable:
        composition = composition.subs('x', function)
    return composition

# not efficient? can't handle len(*args) ~ 10
# https://docs.python.org/3/library/itertools.html#itertools.product
def random_product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
        random.shuffle(result)
    for prod in result:
        yield tuple(prod)

def elementary_function_generator(max_compositions, functions_space=None):
    if functions_space is None:
        functions_space = itertools.chain(ELEMENTARY_FUNCTIONS, polynomial_generator(count=2))
    generator = random_product(functions_space, repeat=max_compositions)
    return map(compose, generator)

def polynomial_generator(count=5, max_order=3, min_coefficient=1, max_coefficient=5, coefficient_space=None):
    if coefficient_space is None:
        coefficient_space = range(min_coefficient, max_coefficient + 1)
    order = random.randint(1, max_order)
    for i in range(count):
        polynomial = []
        for i in range(order, -1, -1):
            cofficient = random.choice(SIGN) * random.choice(coefficient_space)
            polynomial.append(f'{cofficient}*x**{i}')
        yield sympy.sympify('+'.join(polynomial))

