
from antlr4.error.ErrorListener import ErrorListener


class BlendedErrorListener(ErrorListener):
    
    def __init__(self):
        super(BlendedErrorListener,self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        message = "line " + str(line) + ":" + str(column) + " " + msg
        self.errors.append(message)

