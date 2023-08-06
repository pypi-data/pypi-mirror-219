import sys

from antlr4 import *
from antlr4.tree.Trees import Trees

from antlr4.error.ErrorListener import ErrorListener

is_py3k = sys.version_info[0] > 2

if is_py3k:
    from blended.lint.blended_grammar.py3.blendedLexer import blendedLexer
    from blended.lint.blended_grammar.py3.blendedParser import blendedParser
else:
    from blended.lint.blended_grammar.py2.blendedLexer import blendedLexer
    from blended.lint.blended_grammar.py2.blendedParser import blendedParser


from blended.lint.listeners import BlendedErrorListener
    
def lint(input):
    error_listener = BlendedErrorListener() 

    lexer = blendedLexer(input)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)

    parser = blendedParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.start()

    return error_listener.errors
#error_listener.errors = []

