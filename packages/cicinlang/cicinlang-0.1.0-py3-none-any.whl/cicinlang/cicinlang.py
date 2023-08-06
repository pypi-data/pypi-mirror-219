from cicinlang.lexer import Lexer 
from cicinlang.parser_ import Parser
from cicinlang.interpreter import Interpreter
from cicinlang.utils import Context, SymbolTable

global_context = Context( '<module>', None, None )
global_symbol_table = SymbolTable( global_context )
global_context.set_symbol_table( global_symbol_table )

def run( fn, ftext ):
    lexer = Lexer( fn, ftext )
    tokens, error = lexer.create_tokens()

    if error: return None, error 

    if len( tokens ) == 1: return '', None 

    parser = Parser( tokens )
    ast_list, error = parser.parse()

    if error: return None, error 

    interpreter = Interpreter()
    res, error = interpreter.interpret( ast_list, global_context )

    if error: return None, error

    return res, None