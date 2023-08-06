parser grammar blendedParser;

options { tokenVocab=blendedLexer;}

start
    :   ((extendsStatement blockStatementWithParent*)|blendedBlock*) EOF;


blendedBlock
    :    (blended|blockStatement);   

blendedBlockParent
    :    (blended|blockStatementWithParent);

blended
    :    includeStatement
    |    setStatement
    |    printStatement
    |    forStatement
    |    ifStatement
    |    macroStatement
    |    doStatement
    |    rawStatement
    |    renderStatement
    |    comStatement
    |    commentStatement
//    |    allText
    ;

blendedNoSet
    :    includeStatement
    |    printStatement
    |    forStatement
    |    ifStatement
    |    macroStatement
    |    doStatement
    |    rawStatement
    |    renderStatement
    |    comStatement
    |    commentStatement
//    |    allText
    ;

blockStatementWithParent
    :    blockTag parentTag? blendedBlockParent* endblockTag;
blockStatement
    :    blockTag blendedBlock* endblockTag;
extendsStatement
    :    LTAG EXTENDS (attributeVariable|pathString) RTAG;
commentStatement
    :    commentTag blendedBlockParent* endcommentTag;
comStatement
    :    LCOM RCOM;
rawStatement
    :    RAW ENDRAW;
includeStatement
    :    LTAG INCLUDE (pathString|attributeVariable) IGNORE? (WITH expression)? ONLY? RTAG;
setStatement
    :    LTAG SET setVar RTAG;
macroStatement
    :    macroTag blended* endmacroTag;
ifStatement
    :    ifTag blendedBlock* (elseTag blendedBlock*)? endifTag;
printStatement
    :    LTAG PRINT (setVar|expression) RTAG;
forStatement
    :    (forTag|forItemsTag) blendedNoSet* (elseTag blendedNoSet*)? endForTag;
doStatement
    :    LTAG DO (setVar|expression) RTAG;
renderStatement
    :    LREN attributeVariable (IFILTER|EFILTER)* RREN;



forTag
    :    LTAG FOR identifier IN expression RTAG;
forItemsTag
    :    LTAG FOR identifier COMMA identifier IN ITEMS LPAREN expression RPAREN RTAG;
endForTag
    :    LTAG ENDFOR RTAG;
blockTag
    :    LTAG BLOCK identifier RTAG;
endblockTag
    :    LTAG ENDBLOCK RTAG;
parentTag
    :    LTAG PARENT RTAG;
macroTag
    :    LTAG MACRO identifier LPAREN (identifier (COMMA identifier)*)? RPAREN RTAG;
endmacroTag
    :    LTAG ENDMACRO RTAG;
ifTag
    :    LTAG IF expression RTAG;
elseTag
    :    LTAG ELSE RTAG;
endifTag
    :    LTAG ENDIF RTAG;
commentTag
    :    LTAG COMMENT RTAG;
endcommentTag
    :    LTAG ENDCOMMENT RTAG;



pathString
    : (QUOTE path QUOTE|APO path APO);

path
    :    FSLASH? identifier (FSLASH identifier)* DOT identifier;


setVar
    :    identifier ASSIGN expression;


expression
    :LPAREN expression RPAREN
    //|    LREN attributeVariable (IFILTER|EFILTER)* RREN // {{var}} or {{ var.var }}
    |    expression LPAREN (expression (COMMA expression)*)? RPAREN
    |    expression LBRACK expression RBRACK                                              //a[b]
    |    LBRACK expression (COMMA expression)* RBRACK                                     //[a, b, c]
    |    LBRACE expression COLON expression (COMMA expression COLON expression)* RBRACE   //{a:b, c:d}
    |    expression (GT|LT|GE|LE|EQUAL|NOTEQUAL) expression
    |    expression OR expression
    |    expression AND expression
    |    expression IN expression
    |    expression (DOT identifier)+                                                          // a.b
    |    expression CARET expression
    |    expression (MUL|DIV|MOD) expression
    |    expression (ADD|SUB) expression
    |    NOT expression
    |    SUB expression
    |    stringVar
    |    identifier
    ;


attributeVariable
    :    identifier (DOT identifier)*;


stringVar
    :    (APO text APO|QUOTE text QUOTE);

//allText
//    :    (text|APO|QUOTE)+;
identifier
    : (ID            | IN        | AND
    | OR             | NOT       | IGNORE
    | WITH           | ONLY      | BLOCK
    | PARENT         | ENDBLOCK  | INCLUDE
    | EXTENDS        | SET       | PRINT 
    | FOR            | ENDFOR    | MACRO
    | ENDMACRO       | DO        | IF
    | ELSE           | ENDIF     | ITEMS
    | COMMENT        | ENDCOMMENT)+
    ;

text 
//    :    (ID         | COMMA     | POUND
//    |    ASSIGN      | LPAREN    | RPAREN
//    |    ADD         | SUB       | MOD
//    |    MUL         | COLON     | PIPE
//    |    GT          | LT        | DOT
//    |    SEMI        | EXCL      | AT
//    |    BSLASH      | FSLASH    | AMP
//    |    IN          | AND       | OR
//    |    NOT         | IGNORE    | WITH
//    |    ONLY        | BLOCK     | PARENT
//    |    ENDBLOCK    | INCLUDE   | EXTENDS
//    |    SET         | PRINT     | FOR
//    |    ENDFOR      | MACRO     | ENDMACRO
//    |    DO          | IF        | ELSE
//    |    ENDIF       | ITEMS     | COMMENT
//    |    ENDCOMMENT  | LBRACE    | RBRACE )+
    :    ~(RTAG|RREN|TWIG)+
    ;


