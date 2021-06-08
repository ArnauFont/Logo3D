grammar logo3d;
root: (func)* EOF ;

func: FUNCTION ID paramsFunc IS stat+ END;

params:'(' expr (',' expr)* ')'
	|  '(' ')';

paramsFunc: '(' ID (',' ID)* ')' | '(' ')';

stat : ID ASSIG expr									#Assignacio
	| READ expr											#Read
	| WRITE expr										#Write
	| IF cond THEN (stat)+ END							#Condicional
	| IF cond THEN (stat)+ ELSE (stat)+ END 			#CondicionalElse
	| WHILE cond DO (stat)+ END							#While
	| FOR ID FROM expr TO expr DO (stat)+ END			#For
	| expr												#Expressio
	;

expr:
	<assoc = right> expr POW expr 	
	| expr (MUL | DIV) expr			
	| expr (MES | RES) expr	
	| NUM '.' NUM		
    | NUM
	| ID params*					
    ;

cond : expr (L|LE|EQ|NE|GE|G) expr;

ASSIG: ':=';
NUM : [0-9]+ ;
MES: '+';
RES: '-';
MUL: '*';
DIV: '/';
POW: '**';

L:'<';
LE: '<=';
EQ: '==';
NE: '!=';
GE: '>=';
G:'>';

READ: '>>';
WRITE: '<<';
IF: 'IF';
THEN: 'THEN';
END: 'END';
WHILE:'WHILE';
DO:'DO';
FUNCTION: 'PROC';
RETURN:'return';
IS:'IS';
ELSE:'ELSE';
FOR:'FOR';
FROM:'FROM';
TO:'TO';

ID: [A-Za-z0-9_]+;

WS : [ \r\t\n]+ -> skip ;

LINE_COMMENT: '//' ~[\r\n]* -> skip;