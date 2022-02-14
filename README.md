## About
This repository contains code for 'zadanko' - a python3 script that is capable of generating math worksheets with answers.

## Requirements
- python3
- [sympy](https://www.sympy.org/en/index.html)
- a LaTeX compiler (e.g. [pdflatex](https://man.archlinux.org/man/pdftex.1))
- some-kind of a document viewer (e.g. [zathura](https://pwmt.org/projects/zathura/))

## Installation
```bash
git clone https://github.com/jacadzaca/zadanko && cd zadanko && python3 -m pip install -r requirements.txt
```

## Examples
##### Generate a worksheet on quadratics

```python
#!/usr/bin/env python3
import random
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import quadratics


Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def main():
    # generate diffrent kinds of quadratic equations
    zero_solutions_quadratics = [quadratics.generate_quadratic_zero_solutions() for i in range(10)]
    one_solution_quadratics = [quadratics.generate_quadratic_one_solution() for i in range(10)]
    two_solutions_quadratics = [quadratics.generate_quadratic_two_solutions() for i in range(6)]
    # sort them according to 'difficulty' - the greater the sum of quadratic's coefficients, the more difficult it is
    zero_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    one_solution_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    two_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)

    # arrange the problems in random order, but try to keep the problem's difficulty incremental
    problem_lists = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    problems = []
    for _ in range(len(zero_solutions_quadratics) + len(one_solution_quadratics) + len(two_solutions_quadratics)):
        choice = random.choice(problem_lists)
        problems.append(choice.pop())
        if not choice:
            problem_lists.remove(choice)

    # generate the awnsers with sympy https://docs.sympy.org/latest/index.html
    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in problems)
    # generate LaTeX code
    problems = map(sympy.printing.latex, problems)

    #output latex code
    latex = ENV.get_template('problem_sheet.jinja.tex').render(tasks=[Task('Find the roots of function $f$, given by expression:', problems, awnsers)])
    print(latex)

if __name__ == '__main__':
    main()
```

##### Generate a worksheet on differentiation

```python
#!/usr/bin/env python3
import itertools
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import elementary_functions


Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def main():
    # generate 10 elementary functions that are made out of 2 composite functions and append them to the problem list
    problems = take(elementary_functions.elementary_function_generator(2), 10)
    # generate 10 elementary functions that are at most made out of 2 composite functions and then append the multiplication of them to the problem list
    for function, function1 in zip(take(elementary_functions.elementary_function_generator(2), 10), take(elementary_functions.elementary_function_generator(2), 10)):
        problems.append(function * function1)
    # generate 6 elementary functions that are madeout of 3 composite functions and append them to the problem list
    problems += take(elementary_functions.elementary_function_generator(3), 6)
    # sort them by how 'complicated' they are - the more 'composite', the later it's in the list
    problems.sort(key=sympy.count_ops)
    # differentiate and generate LaTeX code
    awnsers = (sympy.printing.latex(function.diff()) for function in problems)
    # generate LaTeX code for problem statments
    problems = map(sympy.printing.latex, problems)

    # output the LaTeX code
    latex = ENV.get_template('problem_sheet.jinja.tex').render(tasks=[Task('Find the derivative of function $f$, given by expression:', problems, awnsers)])
    print(latex)

if __name__ == '__main__':
    main()
```

##### Generate a worksheet on integration

```python
#!/usr/bin/env python3
import collections
import itertools

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import elementary_functions


Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def take_if(condition, iterable):
    for element in iterable:
        if condition(element):
            yield element
        else:
            continue

def main():
    # generate awnsers first - it's easier to ensure the problems will be integrable that way
    awnsers = take(take_if(lambda expr: expr.diff() != 1, elementary_functions.elementary_function_generator(2)), 16)
    random_functions = itertools.cycle(elementary_functions.elementary_function_generator(1))
    for function, function1 in zip(take(random_functions, 10), take(random_functions, 10)):
        awnsers.append(function * function1)
    awnsers.sort(key=sympy.count_ops)
    # generate problems
    problems = (sympy.printing.latex(function.diff()) for function in awnsers)
    awnsers = map(sympy.printing.latex, awnsers)

    integration_task = Task('Integrate function $f$, given by expression:', problems, awnsers)

    latex = ENV.get_template('problem_sheet.jinja.tex').render(tasks=[integration_task])
    print(latex)

if __name__ == '__main__':
    main()
```

##### Generate a worksheet that is the combination of the above worksheets

```python
#!/usr/bin/env python3
import random
import itertools
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import quadratics
from zadanko import elementary_functions

Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))

def take_if(condition, iterable):
    for element in iterable:
        if condition(element):
            yield element
        else:
            continue

def genereate_quadratics_task():
    zero_solutions_quadratics = [quadratics.generate_quadratic_zero_solutions() for i in range(10)]
    one_solution_quadratics = [quadratics.generate_quadratic_one_solution() for i in range(10)]
    two_solutions_quadratics = [quadratics.generate_quadratic_two_solutions() for i in range(6)]
    zero_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator, reverse=True)
    one_solution_quadratics.sort(key=quadratics.quadratic_difficulty_comperator, reverse=True)
    two_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator, reverse=True)

    problem_lists = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    problems = []
    for _ in range(len(zero_solutions_quadratics) + len(one_solution_quadratics) + len(two_solutions_quadratics)):
        choice = random.choice(problem_lists)
        problems.append(choice.pop())
        if not choice:
            problem_lists.remove(choice)

    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in problems)
    problems = map(sympy.printing.latex, sorted(problems, key=quadratics.quadratic_difficulty_comperator))
    return Task('Find roots of function $f$, given by expression:', problems, awnsers)

def generate_differentiation_task():
    differentiation_problems = take(elementary_functions.elementary_function_generator(2), 10)
    for function, function1 in zip(take(elementary_functions.elementary_function_generator(2), 10), take(elementary_functions.elementary_function_generator(2), 10)):
        differentiation_problems.append(function * function1)
    differentiation_problems += take(elementary_functions.elementary_function_generator(3), 6)
    differentiation_problems.sort(key=sympy.count_ops)
    awnsers = (sympy.printing.latex(function.diff()) for function in differentiation_problems)
    differentiation_problems = map(sympy.printing.latex, differentiation_problems)
    return Task('Find the derivative of function $f$, given by expression:', differentiation_problems, awnsers)

def main():
    awnsers = take(take_if(lambda expr: expr.diff() != 1, elementary_functions.elementary_function_generator(2)), 16)
    random_functions = itertools.cycle(elementary_functions.elementary_function_generator(1))
    for function, function1 in zip(take(random_functions, 10), take(random_functions, 10)):
        awnsers.append(function * function1)
    awnsers.sort(key=sympy.count_ops)
    problems = (sympy.printing.latex(function.diff()) for function in awnsers)
    awnsers = map(sympy.printing.latex, awnsers)

    integration_task = Task('Integrate function $f$, given by expression:', problems, awnsers)

    latex = ENV.get_template('problem_sheet.jinja.tex').render(tasks=[genereate_quadratics_task(), generate_differentiation_task(), integration_task])
    print(latex)

if __name__ == '__main__':
    main()
```

To compile the examples use:
```bash
chmod +x example.py && ./example.py | pdflatex --jobname worksheet --output-directory /tmp && zathura /tmp/worksheet.pdf
```

## Legal Note
The code is licensed under [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.txt).

