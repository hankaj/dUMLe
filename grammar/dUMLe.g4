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
    | list_access
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
    | block
    | use_case;

list_declaration
    : '[' BR* ((NAME | obj_access) BR* (',' BR* (NAME | obj_access))*)? BR* ']';
    
list_access
    : NAME '[' DIGIT+ ']' BR*;
    
named_list_declaration
    : NAME BR+ (fun_call | list_declaration) BR* NL;

fun_declaraion
    : 'def' BR+ NAME '(' BR* arg_list BR* ')' BR* ':' BR* NL
        (IND+ instruction NL*)*
        IND+ 'return' BR+ list_declaration BR* NL;
        
fun_call
    : NAME '(' BR* arg_list BR* ')' BR*;

execution
    : 'exec' BR+ NAME (BR+ ('brief' | 'all'))? (BR+ (list_declaration | list_access | NAME | obj_access))? (BR+ TEXT)? BR* NL;
    
loop
    : 'for' BR+ NAME BR+ 'in' BR+ (NAME | list_declaration | obj_access | fun_call) BR* ':' BR* NL
        (IND+ instruction NL)+;
        
connection
    : (NAME | obj_access | list_access) BR+ (ARROW | CONNECTION_TYPE) BR+ (NAME | obj_access | list_access) (BR+ 'labeled' BR+ TEXT )? BR* NL*;
    
block_operation
    : BLOCK_OPERATION_TYPE BR+ (NAME | obj_access | list_access) BR* NL;
    
obj_access
    : NAME '.' (NAME | obj_access);

class_declaration
    : CLASS_TYPE (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (class_declaration_line)+;

class_declaration_line:
    IND+ (MODIFIER BR+)? TEXT BR* NL;

note
    : 'note' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ TEXT BR* NL)+;

actor
    : 'actor' (BR+ NAME)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

theme
    : 'theme' BR+ NAME BR* ':' BR* NL
    (IND+ PARAM_TYPE BR+ TEXT BR* NL)+;

package_declaration
    : 'package' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ (NAME | obj_access | list_access) BR* NL)+;
    
//interface_declaration
//    : 'interface' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
//    (IND+ TEXT BR* NL)+;

arg_list
    : (NAME BR* (',' BR* NAME)*)?;
    
block
    : 'block' (BR+ NAME)? BR+ NAME (BR+ 'labeled' BR+ TEXT )? BR* NL;

use_case
    : 'usecase' (BR+ NAME)? BR+ NAME BR* ':' BR* NL
    (IND+ TEXT BR* NL)+;

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