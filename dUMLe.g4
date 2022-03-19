grammar dUMLe;

program
    : (WS* (instruction | diagcreation) WS*)* EOF;

diagcreation
    : class_diagram
    | seq_diagram
    | use_case_diagram;
    
class_diagram
    : 'diagclass' BR NAME BR* ':' NL (IND instruction NL)+;

seq_diagram
    : 'diagseq' BR NAME BR* ':' NL (IND instruction NL)+;

use_case_diagram
    : 'diagusecase' BR NAME BR* ':' NL (IND instruction NL)+;
    
instruction
    : obj_declaration
    | list_declaration
    | named_list_declaration
    | fun_declaraion
    | fun_call
    | execution
    | loop
    | connection
    | block_operation;

obj_declaration
    : class
    | note
    | actor
    | theme
    | package
    | interface
    | block;

list_declaration
    : '[' BR* ((NAME | obj_access) BR* (',' BR* (NAME | obj_access))*)? BR* ']';
    
named_list_declaration
    : NAME BR list_declaration BR* NL;

fun_declaraion
    : 'def' BR NAME '(' BR* arg_list BR* ')' BR* ':' BR* NL
        (IND instruction NL)+
        IND 'return' BR arg_list NL;
        
fun_call
    : NAME '(' BR* arg_list BR* ')' BR* NL;

execution
    : 'exec' BR NAME (BR ('brief' | 'all'))? (BR (list_declaration | NAME | obj_access))? (BR (QUOTE FILENAME QUOTE))? BR* NL;
    
loop
    : 'for' BR NAME BR 'in' BR (NAME | list_declaration | obj_access) BR* ':' BR* NL
        (IND instruction NL)+;
        
connection
    : (NAME | obj_access) BR (ARROW | CONNECTIONTYPE) BR (NAME | obj_access) BR ('labeled' BR QUOTE TEXT QUOTE)? BR* NL;
    
block_operation
    : ('activate' | 'destroy') BR (NAME | obj_access) BR* NL;
    
obj_access
    : NAME '.' (NAME | obj_access);

class
    : ('class' | 'abstract') (BR NAME)? BR NAME BR* ':' BR* NL
    (IND ('function')? (BR ('public' | 'protected' | 'private'))? BR TEXT BR* NL)+;

note
    : 'note' (BR NAME)? BR NAME BR* ':' BR* NL
    (IND TEXT BR* NL)+;

actor
    : 'actor' (BR NAME)? BR NAME BR ('labeled' BR QUOTE TEXT QUOTE)? BR* NL;

theme
    : 'theme' BR NAME BR* ':' BR* NL
    (IND param_type BR TEXT BR* NL)+;
    
package
    : 'package' (BR NAME)? BR NAME BR* ':' BR* NL
    (IND NAME BR* NL)+;
    
interface
    : 'interface' (BR NAME)? BR NAME BR* ':' BR* NL
    (IND TEXT BR* NL)+;

arg_list
    : (NAME BR* (',' BR* NAME)*)?;
    
block
    : 'block' (BR NAME)? BR NAME BR ('labeled' BR QUOTE TEXT QUOTE)? BR* NL;

param_type
    : ('fontcolor' | 'backgroundcolor' | 'fontsize' | 'font'| 'bordercolor');
    
WS 				
	:
	'\n' 
	| ' ' 
	| '\t';

CR
	: 
	'\r' -> skip;

COM_SIGN 		
	: 
	'#' ~[\r\n]* -> skip;

BR
    :
    ' '+; 
    
NAME
    :
    [A-Za-z_][a-zA-Z0-9_]*;
    
NL
    :
    '\n';
    
IND
    :
    '\t';
    
QUOTE
    :
    '\''|
    '"';
    
FILENAME
    :
    TEXT'.'('png'|'jpg');
    
ARROW
    : 
    ('x<' | '<' | '<<' | '\\' | '//' | '\\\\' | 'o<' | '\\\\o')?
    ('.' | '-' | '_')
    ('>x' | '>' | '>>' | '\\' | '//' | '\\\\' | '>o' | 'o\\\\');
    
CONNECTIONTYPE
    :
    'inherit'
     | 'implement'
     | 'associate'
     | 'depend'
     | 'aggregate'
     | 'compose';
    
TEXT
    : 
    (~[\r\n"])+;