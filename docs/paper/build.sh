#!/bin/bash

# Compile the LaTeX document
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Clean up auxiliary files
rm -f *.aux *.log *.bbl *.blg *.out 