grammar dUMLe;

program
    : ((BR | NL)* (instruction | diagcreation) (BR | NL)*)* EOF;

diagcreation
    : class_diagram
    | seq_diagram
    | use_case_diagram;
    
class_diagram
    : 'diagclass' BR+ NAME BR* ':' BR* NL
    (IND+ instruction BR* NL*)+;

seq_diagram
    : 'diagseq' BR+ NAME BR* ':' BR* NL
    (IND+ instruction BR* NL*)+;

use_case_diagram
    : 'diagusecase' BR+ NAME BR* ':' BR* NL
    (IND+ instruction BR* NL*)+;
    
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
    : class_declaration
    | note
    | actor
    | theme
    | package_declaration
    | interface_declaration
    | block
    | use_case;

list_declaration
    : '[' BR* ((NAME | obj_access) BR* (',' BR* (NAME | obj_access))*)? BR* ']';
    
named_list_declaration
    : NAME BR+ (fun_call | list_declaration) BR* NL;

fun_declaraion
    : 'def' BR+ NAME '(' BR* arg_list BR* ')' BR* ':' BR* NL
        (IND+ instruction NL*)*
        IND+ 'return' BR+ list_declaration BR* NL;
        
fun_call
    : NAME '(' BR* arg_list BR* ')' BR*;

execution
    : 'exec' BR+ NAME (BR+ ('brief' | 'all'))? (BR+ (list_declaration | NAME | obj_access))? (BR+ TEXT)? BR* NL;
    
loop
    : 'for' BR+ NAME BR+ 'in' BR+ (NAME | list_declaration | obj_access | fun_call) BR* ':' BR* NL
        (IND+ instruction NL*)+;
        
connection
    : (NAME | obj_access) BR+ (ARROW | connection_type) BR+ (NAME | obj_access) (BR+ 'labeled' BR+ TEXT )? BR* NL;
    
block_operation
    : ('activate' | 'destroy') BR+ (NAME | obj_access) BR* NL;
    
obj_access
    : NAME '.' (NAME | obj_access);

class_declaration
    : ('class' | 'abstract') (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ (('public' | 'protected' | 'private') BR+)? ('function' BR+)? TEXT BR* NL)+;

note
    : 'note' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ TEXT BR* NL)+;

actor
    : 'actor' (BR+ NAME)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

theme
    : 'theme' BR+ NAME BR* ':' BR* NL
    (IND+ param_type BR+ TEXT BR* NL)+;
    
package_declaration
    : 'package' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ (NAME | obj_access) BR* NL)+;
    
interface_declaration
    : 'interface' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ ('function' BR+) TEXT BR* NL)+;

arg_list
    : (NAME BR* (',' BR* NAME)*)?;
    
block
    : 'block' (BR+ NAME)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

use_case
    : 'usecase' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ TEXT BR* NL)+;

param_type
    : ('fontcolor' | 'backgroundcolor' | 'fontsize' | 'font'| 'bordercolor');

connection_type
    :
    'inherit'
     | 'implement'
     | 'associate'
     | 'depend'
     | 'aggregate'
     | 'compose';

CR
	: 
	'\r' -> skip;

COM_SIGN 		
	: 
	'#' ~[\r\n]* -> skip;

BR
    :
    ' ';
    
NAME
    :
    [A-Za-z_][a-zA-Z0-9_]*;
    
NL
    :
    '\n';
    
IND
    :
    '\t'
    | '    ';
    
QUOTE
    :
    '\''|
    '"';
    
ARROW
    : 
    ('x<' | '<' | '<<' | '\\' | '//' | '\\\\' | 'o<' | '\\\\o')?
    ('.' | '-' | '_')
    ('>x' | '>' | '>>' | '\\' | '//' | '\\\\' | '>o' | 'o\\\\');
    
TEXT
    : 
    QUOTE (~[\r\n"])+ QUOTE;