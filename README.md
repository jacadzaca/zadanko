## About
This repository contains code for 'zadanko' - a set of python3 scripts that generate math worksheets with answers.

## Requirements
- python3
- [sympy](https://www.sympy.org/en/index.html)
- [jinja2](https://jinja.palletsprojects.com/)
- a LaTeX compiler (e.g. [pdflatex](https://man.archlinux.org/man/pdftex.1))
- some-kind of a document viewer (e.g. [zathura](https://pwmt.org/projects/zathura/))

## Installation
First ensure you have pdflatex and a document viewer
```bash
apt install texlive-latex-base texlive-fonts-recommended zathura # debian et al.
pacman -Syy texlive-most zathura # arch
```
Install zadanko:
```bash
git clone https://github.com/jacadzaca/zadanko && cd zadanko && python3 -m pip install -r requirements.txt .
```

## Examples
##### [Generate a worksheet on quadratics](https://raw.githubusercontent.com/jacadzaca/zadanko/master/examples/generate_quadratics_worksheet.py)

```python
#!/usr/bin/env python3
import random
import collections

import sympy
from jinja2 import Environment, PackageLoader

from zadanko import quadratics

Task = collections.namedtuple('Task', ['instruction', 'problems', 'awnsers'])

ENV = Environment(
    loader=PackageLoader('zadanko'),
    trim_blocks=True,
    lstrip_blocks=True)

def generate_quadratics_task():
    # generate diffrent kinds of quadratic equations
    zero_solutions_quadratics = [quadratics.generate_quadratic_zero_solutions() for _ in range(10)]
    one_solution_quadratics = [quadratics.generate_quadratic_one_solution() for _ in range(10)]
    two_solutions_quadratics = [quadratics.generate_quadratic_two_solutions() for _ in range(6)]
    # sort them according to 'difficulty' - the greater the sum of quadratic's coefficients, the more difficult it is
    zero_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    one_solution_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)
    two_solutions_quadratics.sort(key=quadratics.quadratic_difficulty_comperator)

    # arrange the problems in random order, but try to keep the problem's difficulty incremental
    problems = []
    problem_lists = [zero_solutions_quadratics, one_solution_quadratics, two_solutions_quadratics]
    for _ in range(sum(map(len, problem_lists))):
        choice = random.choice(problem_lists)
        problems.append(choice.pop())
        if not choice:
            problem_lists.remove(choice)

    # generate the awnsers with sympy https://docs.sympy.org/latest/index.html
    awnsers = (sympy.printing.latex((sympy.solvers.solveset(quadratic, domain=sympy.S.Reals))) for quadratic in problems)
    # generate LaTeX code
    problems = map(sympy.printing.latex, problems)
    return Task('Find the roots of function $f$, given by expression:', problems, awnsers)

if __name__ == '__main__':
    #output latex code
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_quadratics_task()])
    print(latex)
```

##### [Generate a worksheet on differentiation](https://raw.githubusercontent.com/jacadzaca/zadanko/master/examples/generate_differentiation_worksheet.py)

```python
#!/usr/bin/env python3
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
```

##### [Generate a worksheet on integration](https://raw.githubusercontent.com/jacadzaca/zadanko/master/examples/generate_integration_worksheet.py)

```python
#!/usr/bin/env python3
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
```

##### [Generate a worksheet that is the combination of the above worksheets](https://raw.githubusercontent.com/jacadzaca/zadanko/master/examples/generate_combination_worksheet.py)

```python
#!/usr/bin/env python3
# keep in mind this depends on the previous scripts

from jinja2 import Environment, PackageLoader

from generate_quadratics_worksheet import generate_quadratics_task
from generate_differentiation_worksheet import generate_differentiation_task
from generate_integration_worksheet import generate_integration_task

ENV = Environment(
    loader=PackageLoader('zadanko', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

if __name__ == '__main__':
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_quadratics_task(), generate_differentiation_task(), generate_integration_task()])
    print(latex)
```

To compile use:
```bash
chmod +x example.py && ./example.py | pdflatex --jobname worksheet --output-directory /tmp && zathura /tmp/worksheet.pdf
```
See [examples](https://github.com/jacadzaca/zadanko/tree/master/examples) for more

## Legal Note
The code is licensed under [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.txt).

