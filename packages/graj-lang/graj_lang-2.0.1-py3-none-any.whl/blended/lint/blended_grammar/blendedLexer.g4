lexer grammar blendedLexer;

RAW           : '{% raw %}' -> pushMode(RAW);
LCOM          : '{#' -> pushMode(COM);
LTAG          : '{%' -> pushMode(TAG);
LREN          : '{{' -> pushMode(REN);
DOT           : '.' -> skip;
RREN          : '}}' -> skip;
TWIG          : '#{' -> skip;
ID            : ([a-zA-Z]|[0-9]|'_')+ -> skip;
IN            : 'in';
AND           : 'and';
OR            : 'or';
NOT           : 'not';
IGNORE        : 'ignore missing' -> skip;
WITH          : 'with' -> skip;
ONLY          : 'only' -> skip;
BLOCK         : 'block' -> skip;
PARENT        : 'parent' -> skip;
ENDBLOCK      : 'endblock' -> skip;
INCLUDE       : 'include' -> skip;
EXTENDS       : 'extends' -> skip;
SET           : 'set' -> skip;
PRINT         : 'print' -> skip;
FOR           : 'for' -> skip;
ENDFOR        : 'endfor' -> skip;
MACRO         : 'macro' -> skip;
ENDMACRO      : 'endmacro' -> skip;
DO            : 'do' -> skip;
IF            : 'if' -> skip;
ELSE          : 'else' -> skip;
ENDIF         : 'endif' -> skip;
ITEMS         : 'items' -> skip;
COMMENT       : 'comment' -> skip;
ENDCOMMENT    : 'endcomment' -> skip;
TEXT          : . -> skip;
WS            : [ \t]+ -> skip ; // toss out whitespace
NEWLINE       : ('\r'? '\n')+ -> skip ;     // return newlines to parser (is end-statement signal)


mode RAW;
ENDRAW        : '{% endraw %}' -> popMode;
RAW_TEXT      : TEXT -> type(TEXT),skip;
RAW_WS        : WS -> type(WS),skip;
RAW_NEWLINE   : NEWLINE -> type(NEWLINE),skip;     // return newlines to parser (is end-statement signal)

mode COM;
RCOM          : '#}' -> popMode;
COM_TEXT      : TEXT -> type(TEXT),skip;
COM_WS        : WS -> type(WS),skip;
COM_NEWLINE   : NEWLINE -> type(NEWLINE),skip;     // return newlines to parser (is end-statement signal)

mode REN;
REN_RREN      : RREN -> type(RREN),popMode;
EFILTER       : '|e';
IFILTER       : '|items';
REN_DOT       : DOT -> type(DOT);
REN_IN        : IN -> type(IN);
REN_AND       : AND -> type(AND);
REN_OR        : OR -> type(OR);
REN_NOT       : NOT -> type(NOT);
REN_IGNORE    : IGNORE -> type(IGNORE);
REN_WITH      : WITH -> type(WITH);
REN_ONLY      : ONLY -> type(ONLY);
REN_BLOCK     : BLOCK -> type(BLOCK);
REN_PARENT    : PARENT -> type(PARENT);
REN_ENDBLOCK  : ENDBLOCK -> type(ENDBLOCK);
REN_INCLUDE   : INCLUDE -> type(INCLUDE);
REN_EXTENDS   : EXTENDS -> type(EXTENDS);
REN_SET       : SET -> type(SET);
REN_PRINT     : PRINT -> type(PRINT);
REN_FOR       : FOR -> type(FOR);
REN_ENDFOR    : ENDFOR -> type(ENDFOR);
REN_MACRO     : MACRO -> type(MACRO);
REN_ENDMACRO  : ENDMACRO -> type(ENDMACRO);
REN_DO        : DO -> type(DO);
REN_IF        : IF -> type(IF);
REN_ELSE      : ELSE -> type(ELSE);
REN_ENDIF     : ENDIF -> type(ENDIF);
REN_ITEMS     : ITEMS -> type(ITEMS);
REN_COMMENT   : COMMENT -> type(COMMENT);
REN_ENDCOMMENT: ENDCOMMENT -> type(ENDCOMMENT);
REN_ID        : ID -> type(ID);
REN_WS        : WS -> type(WS),skip;  // toss out whitespace
REN_NEWLINE   : NEWLINE -> type(NEWLINE),skip;     // return newlines to parser (is end-statement signal)

mode TAG;
TAG_RREN        : RREN -> type(RREN);
TAG_IN          : IN -> type(IN);
TAG_TWIG        : TWIG -> type(TWIG);
TAG_AND         : AND -> type(AND);
TAG_OR          : OR -> type(OR);
TAG_NOT         : NOT -> type(NOT);
TAG_IGNORE      : IGNORE -> type(IGNORE);
TAG_WITH        : WITH -> type(WITH);
TAG_ONLY        : ONLY -> type(ONLY);
TAG_BLOCK       : BLOCK -> type(BLOCK);
TAG_PARENT      : PARENT -> type(PARENT);
TAG_ENDBLOCK    : ENDBLOCK -> type(ENDBLOCK);
TAG_INCLUDE     : INCLUDE -> type(INCLUDE);
TAG_EXTENDS     : EXTENDS -> type(EXTENDS);
TAG_SET         : SET -> type(SET);
TAG_PRINT       : PRINT -> type(PRINT);
TAG_FOR         : FOR -> type(FOR);
TAG_ENDFOR      : ENDFOR -> type(ENDFOR);
TAG_MACRO       : MACRO -> type(MACRO);
TAG_ENDMACRO    : ENDMACRO -> type(ENDMACRO);
TAG_DO          : DO -> type(DO);
TAG_IF          : IF -> type(IF);
TAG_ELSE        : ELSE -> type(ELSE);
TAG_ENDIF       : ENDIF -> type(ENDIF);
TAG_ITEMS       : ITEMS -> type(ITEMS);
TAG_COMMENT     : COMMENT -> type(COMMENT);
TAG_ENDCOMMENT  : ENDCOMMENT -> type(ENDCOMMENT);
//IGNORE        : 'ignore missing';
//WITH          : 'with';
//ONLY          : 'only';
//BLOCK         : 'block';
//PARENT        : 'parent';
//ENDBLOCK      : 'endblock';
//INCLUDE       : 'include';
//EXTENDS       : 'extends';
//SET           : 'set';
//PRINT         : 'print';
//FOR           : 'for';
//ENDFOR        : 'endfor';
//MACRO         : 'macro';
//ENDMACRO      : 'endmacro';
//DO            : 'do';
//IF            : 'if';
//ELSE          : 'else';
//ENDIF         : 'endif';
//ITEMS         : 'items';


//Special Characters
RTAG          : '%}' -> popMode;
TAG_LREN      : '{{' -> type(LREN);//, pushMode(REN);
QUOTE         : '"';
APO           : '\'';
LPAREN        : '(';
RPAREN        : ')';
LBRACE        : '{';
RBRACE        : '}';
LBRACK        : '[';
RBRACK        : ']';
COMMA         : ',';
TAG_DOT       : DOT -> type(DOT);
//UNDERSCORE    : '_';
AMP           : '&';
BSLASH        : '\\';
FSLASH        : '/';
SEMI          : ';';
PIPE          : '|';
EXCL          : '!';
AT            : '@';
POUND         : '#';


//Operators
ASSIGN        : '=';
COLON         : ':';
//IN            : 'in';
//AND           : 'and';
//OR            : 'or';
//NOT           : 'not';
EQUAL         : '==';
NOTEQUAL      : '!=';
GT            : '>';
LT            : '<';
LE            : '<=';
GE            : '>=';
ADD           : '+';
SUB           : '-';
MUL           : '*';
DIV           : '/';
CARET         : '^';
MOD           : '%';

TAG_ID        : ID -> type(ID);
//ID            : ([a-zA-Z]|[0-9])+;
//NEWLINE       : ['\r'? '\n']+ -> skip ;     // return newlines to parser (is end-statement signal)
////LETTERS     : [a-zA-Z]+ ;      // match identifiers <label id="code.tour.expr.3"/>
////DIGITS      : [0-9]+ ;         // match integers


TAG_NEWLINE   : NEWLINE -> type(NEWLINE),skip;     // return newlines to parser (is end-statement signal)
TAG_WS        : WS -> type(WS),skip;  // toss out whitespace
