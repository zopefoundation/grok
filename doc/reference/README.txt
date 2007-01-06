=========================
The grok reference manual
=========================

The manual is written using LaTeX with support for the Python documentation
markup. The tex sources can be compiled to HTML and PDF. To build the manual,
you need the 'mkhowto' script from a recent Python source distribution.

Build the HTML
--------------

  $ mkhowto --html reference.tex

The directory 'reference/' keeps all files required to display the manual after
that call and can be put on a static webserver.

Build the PDF
-------------

The file 'reference.pdf' will contain the PDF version of the manual after this
call:

  $ mkhowto --pdf reference.tex

