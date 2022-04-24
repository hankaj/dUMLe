grammar dUMLe;

program
    : ((BR | NL)* (instruction | diagcreation) (BR | NL)*)* EOF;

diagcreation
    : class_diagram
    | seq_diagram
    | use_case_diagram;
    
class_diagram
    : 'diagclass' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;

seq_diagram
    : 'diagseq' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;

use_case_diagram
    : 'diagusecase' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;
    
instruction
    : obj_declaration
    | list_declaration
    | list_access
    | named_list_declaration
    | fun_declaration
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
    | block
    | use_case;

list_declaration
    : '[' BR* ((name | obj_access) BR* (',' BR* (name | obj_access))*)? BR* ']';
    
list_access
    : name '[' DIGIT+ ']' BR*;
    
named_list_declaration
    : arg_list BR+ '=' BR+ (fun_call | list_declaration) BR* NL;

fun_declaration
    : 'def' BR+ NAME '(' BR* arg_list* BR* ')' BR* ':' BR* NL
        (NL* IND+ instruction NL*)*
        IND+ 'return' BR+ arg_list BR* NL;
        
fun_call
    : name '(' BR* arg_list_include_scope BR* ')' BR*;

execution
    : 'exec' BR+ NAME (BR+ ('brief' | 'all'))? (BR+ (list_declaration | list_access | NAME | obj_access))? (BR+ TEXT)? BR* NL;

loop
    : 'for' BR+ NAME BR+ 'in' BR+ (name | list_declaration | obj_access | fun_call) BR* ':' BR* NL
        (NL* IND+ instruction NL*)+;
        
connection
    : (name | obj_access | list_access) BR+ (ARROW | CONNECTION_TYPE) BR+ (name | obj_access | list_access) (BR+ 'labeled' BR+ TEXT )? BR* NL*;
    
block_operation
    : BLOCK_OPERATION_TYPE BR+ (name | obj_access | list_access) BR* NL;
    
obj_access
    : name '.' (name | obj_access);

class_declaration
    : CLASS_TYPE (BR+ name)? BR+ NAME BR* ':' BR* NL
    (class_declaration_line)+;

class_declaration_line:
    NL* IND+ (MODIFIER BR+)? TEXT BR* NL*;

note
    : 'note' (BR+ name)? BR+ NAME BR* ':' BR* NL
    (NL* IND+ TEXT BR* NL*)+;

actor
    : 'actor' (BR+ name)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

theme
    : 'theme' BR+ NAME BR* ':' BR* NL
    (NL* IND+ PARAM_TYPE BR+ TEXT BR* NL*)+;

package_declaration
    : 'package' (BR+ name)? BR+ NAME BR* ':' BR* NL
    (NL* IND+ (name | obj_access | list_access) BR* NL*)+;

arg_list
    : NAME BR* (',' BR* NAME)*;

arg_list_include_scope
    : (name BR* (',' BR* name)*)?;
    
block
    : 'block' (BR+ name)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

use_case
    : 'usecase' (BR+ name)? BR+ NAME BR* ':' BR* NL
    (NL* IND+ TEXT BR* NL*)+;

name
    : SCOPE_NAME?NAME;

CLASS_TYPE
    : 'class'
    | 'abstract'
    | 'interface';

PARAM_TYPE
    : 'fontcolor'
    | 'backgroundcolor'
    | 'fontsize'
    | 'font'
    | 'bordercolor';

CONNECTION_TYPE
    :
    'inherit'
     | 'implement'
     | 'associate'
     | 'depend'
     | 'aggregate'
     | 'compose';

MODIFIER
    : 'public'
    | 'protected'
    | 'private';

BLOCK_OPERATION_TYPE
    : 'activate'
    | 'destroy';

CR
	: 
	'\r' -> skip;

COM_SIGN 		
	: 
	'#' ~[\r\n]* -> skip;
	
DIGIT
    :
    [0-9];

BR
    :
    ' ';

SCOPE_NAME
    :
    [A-Za-z_][a-zA-Z0-9_]*'&';

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