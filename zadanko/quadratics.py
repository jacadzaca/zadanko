import math
import sympy
import random

from zadanko import SIGN

def generate_quadratic_two_solutions(max_coefficient=20):
    b = random.randint(3, max_coefficient)
    a = random.randint(1, (b**2)//8)
    c = random.randint(1, (b**2)//(4*a))
    return sympy.sympify(f'{a}*x**2 + {b}*x + {c}')

def generate_quadratic_one_solution(max_coefficient=20):
    sign = random.choice(SIGN)
    a, c = sign * random.randint(1, max_coefficient)**2, sign * random.randint(1, max_coefficient)**2
    b = int(math.sqrt(4*a*c))
    return sympy.sympify(f'{a}*x**2 + {b}*x + {c}')

def generate_quadratic_zero_solutions(max_coefficient=20):
    sign = random.choice(SIGN)
    a, c = sign * random.randint(1, max_coefficient), sign * random.randint(1, max_coefficient)
    b = math.sqrt(random.randint(1, math.floor(math.sqrt(4*a*c))))
    b = sympy.Rational(str(math.trunc(b * 10)/10))
    return sympy.sympify(f'{a}*x**2 + {b}*x + {c}')

def quadratic_difficulty_comperator(x):
    return sum(x.as_coefficients_dict().values())

