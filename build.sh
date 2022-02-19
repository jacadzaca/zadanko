# pipe LaTeX into this
pdflatex --jobname worksheet --output-directory /tmp && zathura /tmp/worksheet.pdf << /dev/stdin
