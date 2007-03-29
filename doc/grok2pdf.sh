#!/bin/sh
rst2latex.py --use-latex-toc --stylesheet=style.tex tutorial.txt > tutorial.tex
pdflatex tutorial.tex
