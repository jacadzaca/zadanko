## About
This repository contains code for 'zadanko' - a python3 script that is capable of generating math worksheets with answers.

## Installation
```bash
git clone https://github.com/jacadzaca/dbcpy && cd zadanko
```

## Examples
##### Generate a worksheet on quadratics

```python
#!/usr/bin/env python3
import math
import sympy
import string
import random

import zadanko.quadratics

from sympy.abc import x
from dataclasses import dataclass
from jinja2 import Environment, PackageLoader

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def main():
    # generate diffrent kinds of quadratic equations
    zero_solutions_quadratics = [zadanko.quadratics.generate_quadratic_zero_solutions() for i in range(10)]
    one_solution_quadratics = [zadanko.quadratics.generate_quadratic_one_solution() for i in range(10)]
    two_solutions_quadratics = [zadanko.quadratics.generate_quadratic_two_solutions() for i in range(6)]
    # sort them according to 'difficulty' - the greater the sum of quadratic's coefficients, the more difficult it is
    zero_solutions_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)
    one_solution_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)
    two_solutions_quadratics.sort(key=zadanko.quadratics.quadratic_difficulty_comperator, reverse=True)

    # arrange the problems in random order, but try to keep the problem's difficulty incremental
    problem_list = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    random_quadratics = []
    for i in range(len(zero_solutions_quadratics) + len(one_solution_quadratics) + len(two_solutions_quadratics)):
        choice = random.choice(problem_list)
        random_quadratics.append(choice.pop())
        if not choice:
            problem_list.remove(choice)

    # generate the awnsers with sympy https://docs.sympy.org/latest/index.html
    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in random_quadratics)
    # generate LaTeX code
    random_quadratics = map(sympy.printing.latex, sorted(random_quadratics, key=zadanko.quadratics.quadratic_difficulty_comperator))

    #output latex code
    latex = ENV.get_template('problems.jinja.tex').render(equations=random_quadratics, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

```

##### Generate a worksheet on differentiation

```python
#!/usr/bin/env python3
import sympy

import zadanko.elementary_functions as elementary_functions

from jinja2 import Environment, PackageLoader

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def main():
    # generate 26 elementary functions that are at most made out of three composite functions
    random_functions = [elementary_functions.generate_elementary_function(min_compositions=1, max_compositions=3) for i in range(26)]
    # sort them by how 'complicated' they are - the more 'composite', the later it's in the list
    random_functions.sort(key=sympy.count_ops)
    # differentiate and generate LaTeX code
    awnsers = (sympy.printing.latex(function.diff()) for function in random_functions)
    # generate LaTeX code for problem statments
    random_functions = map(sympy.printing.latex, random_functions)

    # wrtie the LaTeX code
    latex = ENV.get_template('diffrentiation_problems.jinja.tex').render(equations=random_functions, awnsers=awnsers)
    with open('problems.tex', 'w') as f:
        f.write(latex)

```

## Legal Note
The code is licensed under [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.txt).

