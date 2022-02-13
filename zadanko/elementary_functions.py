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
]


def generate_random_polynomial(max_order=4, max_coefficient=10):
    order = random.randint(1, max_order)
    polynomial = []
    for i in range(order, -1, -1):
        cofficient = random.choice(SIGN) * random.randint(1, max_coefficient)
        polynomial.append(f'{cofficient}*x**{i}')
    return sympy.sympify('+'.join(polynomial))

def generate_elementary_function(min_compositions=1, max_compositions=3):
    function = ID
    for i in range(random.randint(min_compositions, max_compositions)):
        function = function.subs('x', random.choice(ELEMENTARY_FUNCTIONS + [generate_random_polynomial()]))
    return function


