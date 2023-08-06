import string

class Constants:
    LETTERS = string.ascii_letters
    DIGITS = '0123456789'
    OPERATORS = '+-*/^'
    WHITESPACES = ' \t\n'
    PARENTHESES = '()'
    KEYWORDS = { 'var', 'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'input_str', 'input_num', 'print', 'str' }

    AT_OLD = 'OLD'
    AT_NEW = 'NEW'

    TT_INT = 'INT'
    TT_FLOAT = 'FLOAT'
    TT_STRING = 'STRING'

    TT_PLUS = 'PLUS'
    TT_MINUS = 'MINUS'
    TT_MUL = 'MUL'
    TT_DIV = 'DIV'
    TT_EXP = 'EXP'
    TT_LPAREN = 'LPAREN'
    TT_RPAREN = 'RPAREN'
    TT_LBRACE = 'LBRACE'
    TT_RBRACE = 'RBRACE'
    TT_EOF = 'EOF'
    TT_EQ = 'EQ'
    TT_EE = 'EE'
    TT_NE = 'NE'
    TT_GT = 'GT'
    TT_GTE = 'GTE'
    TT_LT = 'LT'
    TT_LTE = 'LTE'
    TT_IDENTIFIER = 'IDENTIFIER'
    TT_KEYWORD = 'KEYWORD'
    TT_SEMICOLON = 'SEMICOLON'
    TT_COMMA = 'COMMA'


class Token:
    def __init__( self, type_, value=None ):
        self.type = type_
        self.value = value 
    
    def __repr__( self ):
        if self.value != None: return f'{self.type}:{self.value}'
        else: return f'{self.type}'

    def set_pos( self, start_pos, end_pos=None ):
        self.start_pos = start_pos 

        if end_pos == None:
            pos = start_pos.copy()
            pos.advance()
            self.end_pos = pos 

        else: 
            self.end_pos = end_pos 
        
        return self 
    

class Position:
    def __init__( self, fn, ftext, idx=-1, ln=0, coln=-1 ):
        self.fn = fn 
        self.ftext = ftext 
        self.idx = idx
        self.ln = ln
        self.coln = coln 

        if self.idx == -1:
            self.advance()
    
    def advance( self ):
        self.idx += 1
        self.coln += 1

        if self.idx > 0 and self.idx <= len( self.ftext ) and self.ftext[self.idx - 1] == '\n':
            self.ln += 1
            self.coln = 0
    
    def copy( self ):
        return Position( self.fn, self.ftext, self.idx, self.ln, self.coln )
    

class Context:
    def __init__( self, name, parent=None, parent_entry_pos=None ):
        self.name = name 
        self.parent = parent 
        self.parent_entry_pos = parent_entry_pos 
        self.symbol_table = None 
    
    def set_symbol_table( self, symbol_table ):
        self.symbol_table = symbol_table


class SymbolTable:
    def __init__( self, context ):
        self.table = {}
        self.context = context 
    
    def get_value( self, key ):
        val = self.table.get( key, None )

        if val == None and self.context.parent != None:
            return self.context.parent.table.get( key, None )

        return val 

    def set_value( self, key, value ):
        self.table[key] = value 

    def remove_value( self, key ):
        del self.table[key]
