grammar dUMLe;

WS 				
	:
	'\n' 
	| ' ' 
	| '\t'
	;

CR
	: 
	'\r' -> skip;

COM_SIGN 		
	: 
	'#' ~[\r\n]* -> skip;

program
    : (WS* (instruction | diagcreation) WS*)* EOF;


instruction
    : obj_declaration
    | list_declaration
    | fun_declaraion
    | function_call
    | execution
    | loop;

diagcreation
    : class_diagram
    | seq_diagram
    | use_case_diagram;

class_diagram
    : 'diagclass' BR NAME BR ':' NL (IND instruction NL)+;

seq_diagram
    : 'diagseq' BR NAME BR ':' NL (IND instruction NL)+;

use_case_diagram
    : 'diagusecase' BR NAME BR ':' NL (IND instruction NL)+;

arg_list
    : (NAME BR (',' BR NAME)*)?;

list_declaration
    : '[' BR arg_list BR ']';

function_declaration
    : 'def' BR NAME '(' BR arg_list BR ')' BR ':' NL
        (IND instruction NL)+
        IND 'return' BR arg_list NL;

obj_declaration
    : class
    | note
    | actor
    | theme
    | package
    | interface
    | block;

class
    : ('class' | 'abstract') (BR NAME)? BR NAME BR ':' NL
    (IND BR ('function')? BR AC BR TEXT BR NL)+;

interface
    : 'interface' (BR NAME)? BR NAME BR ':' NL
    (IND BR TEXT BR NL)+;

note
    : 'note' (BR NAME)? BR NAME BR ':' NL
    (IND BR TEXT BR NL)+;

actor
    : 'actor' (BR NAME)? BR NAME BR ('labeled' BR DELIM TEXT DELIM)? BR NL;

theme
    : 'theme' BR NAME BR ':' BR NL
    (IND param_type BR TEXT_ADD BR NL)+;

package
    : 'package' (BR NAME)? BR NAME BR ':' NL
    (IND NAME BR NL)+;

block
    : 'block' (BR NAME)? BR NAME BR ('labeled' BR DELIM TEXT DELIM)? BR NL;

execution
    :
    ;
    




