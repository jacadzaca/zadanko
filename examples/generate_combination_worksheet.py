#!/usr/bin/env python3
''' Generate a worksheet that contains problems on quadratics, differentiation and integration '''

from jinja2 import Environment, PackageLoader

from generate_quadratics_worksheet import generate_quadratics_task
from generate_differentiation_worksheet import generate_differentiation_task
from generate_integration_worksheet import generate_integration_task

ENV = Environment(
    loader=PackageLoader('zadanko'),
    trim_blocks=True,
    lstrip_blocks=True)

if __name__ == '__main__':
    latex = ENV \
            .get_template('problem_sheet.jinja.tex') \
            .render(tasks=[generate_quadratics_task(), generate_differentiation_task(), generate_integration_task()])
    print(latex)

