from cicinlang.utils import Token, Position, Constants
from cicinlang.errors import IllegalCharException

class Lexer:
    def __init__( self, fn, ftext ):
        self.pos = Position( fn, ftext )
        self.cur_char = ftext[self.pos.idx] if self.pos.idx < len( ftext ) else None
    
    def advance( self ):
        self.pos.advance()
        self.cur_char = self.pos.ftext[self.pos.idx] if self.pos.idx < len( self.pos.ftext ) else None

    def create_tokens( self ):
        tokens = []

        while self.cur_char != None:
            if self.cur_char in Constants.WHITESPACES:
                self.advance()

            elif self.cur_char in Constants.LETTERS:
                tokens.append( self.create_identifier_token() )

            elif self.cur_char in Constants.DIGITS:
                tokens.append( self.create_num_token() )
            
            elif self.cur_char in Constants.OPERATORS:
                tokens.append( self.create_operator_token() )
            
            elif self.cur_char in Constants.PARENTHESES:
                tokens.append( self.create_parentheses_token() )

            elif self.cur_char == '>':
                tokens.append( self.create_greater_than_token() )
            
            elif self.cur_char == '<':
                tokens.append( self.create_less_than_token() )
            
            elif self.cur_char == '=':
                tokens.append( self.create_equals_token() )

            elif self.cur_char == '!':
                token, error = self.create_not_equals_token()

                if error: return None, error 

                tokens.append( token )

            elif self.cur_char == '#':
                while self.cur_char not in  [ '\n', None ]:
                    self.advance()
            
            elif self.cur_char == ';':
                tokens.append( Token( Constants.TT_SEMICOLON ).set_pos( self.pos ) )
                self.advance()

            elif self.cur_char == ',':
                tokens.append( Token( Constants.TT_COMMA ).set_pos( self.pos ) )
                self.advance()

            elif self.cur_char == '{':
                tokens.append( Token( Constants.TT_LBRACE ).set_pos( self.pos ) )
                self.advance()

            elif self.cur_char == '}':
                tokens.append( Token( Constants.TT_RBRACE ).set_pos( self.pos ) )
                self.advance()

            elif self.cur_char in [ "'", '"']:
                tok, error = self.create_string_token()

                if error: return None, error 

                tokens.append( tok )

            else:
                c = "'" + self.cur_char + "'"
                return None, IllegalCharException( c, self.pos )
        
        tokens.append( Token( Constants.TT_EOF ).set_pos( self.pos, self.pos ) )
        return tokens, None 
    
    def create_greater_than_token( self ):
        start_pos = self.pos.copy() 
        tok_type = Constants.TT_GT 
        tok_val = '>'
        self.advance()

        if self.cur_char == '=':
            tok_type = Constants.TT_GTE
            tok_val = '>='
            self.advance()
        
        return Token( tok_type, tok_val ).set_pos( start_pos, self.pos )
        
    def create_less_than_token( self ):
        start_pos = self.pos.copy() 
        tok_type = Constants.TT_LT 
        tok_val = '<'
        self.advance()

        if self.cur_char == '=':
            tok_type = Constants.TT_LTE
            tok_val = '<='
            self.advance()
        
        return Token( tok_type, tok_val ).set_pos( start_pos, self.pos )
    
    def create_equals_token( self ):
        start_pos = self.pos.copy() 
        tok_type = Constants.TT_EQ
        tok_val = None
        self.advance()

        if self.cur_char == '=':
            tok_type = Constants.TT_EE 
            tok_val = '=='
            self.advance()
        
        return Token( tok_type, tok_val ).set_pos( start_pos, self.pos )
    
    def create_not_equals_token( self ):
        start_pos = self.pos.copy() 
        self.advance()
        c = self.cur_char
        self.advance()

        if self.cur_char == '=':
            tok_type = Constants.TT_NE
            tok_val = '!='
            return Token( tok_type ).set_pos( start_pos, self.pos ), None 

        else:
            return None, IllegalCharException( f"'{c}'", start_pos, self.pos )
    
    
    def create_identifier_token( self ):
        id_str = ''
        pos_start = self.pos.copy()
        
        while self.cur_char != None and self.cur_char in Constants.LETTERS + Constants.DIGITS + '_':
            id_str += self.cur_char 
            self.advance()
        
        tok_type = Constants.TT_KEYWORD if id_str in Constants.KEYWORDS else Constants.TT_IDENTIFIER

        return Token( tok_type, id_str ).set_pos( pos_start, self.pos )

    def create_num_token( self ):
        num_str = ''
        dot_count = 0
        start_pos = self.pos.copy()

        while self.cur_char != None and self.cur_char in Constants.DIGITS + '.':
            if self.cur_char == '.':
                if dot_count >= 1: break 
                else: dot_count += 1

            num_str += self.cur_char 
            self.advance()

        if dot_count > 0: return Token( Constants.TT_FLOAT, float( num_str ) ).set_pos( start_pos, self.pos )
        else: return Token( Constants.TT_INT, int( num_str ) ).set_pos( start_pos, self.pos )

    def create_operator_token( self ):
        if self.cur_char == '+':
            type_ = Constants.TT_PLUS
            val = '+'

        elif self.cur_char == '-':
            type_ = Constants.TT_MINUS
            val = '-'

        elif self.cur_char == '*':
            type_ = Constants.TT_MUL
            val = '*'

        elif self.cur_char == '/':
            type_ = Constants.TT_DIV
            val = '/'

        elif self.cur_char == '^':
            type_ = Constants.TT_EXP
            val = '^'
        
        tok = Token( type_, val ).set_pos( self.pos )
        self.advance()
        return tok 

    def create_parentheses_token( self ):
        if self.cur_char == '(':
            type_ = Constants.TT_LPAREN

        elif self.cur_char == ')':
            type_ = Constants.TT_RPAREN
        
        tok = Token( type_ ).set_pos( self.pos )
        self.advance()
        return tok 
    
    def create_string_token( self ):
        end_char = self.cur_char 
        start_pos = self.pos.copy()
        s = ""

        self.advance()

        while self.cur_char != None and self.cur_char != end_char:
            s += self.cur_char
            self.advance()
        
        if self.cur_char == None:
            if end_char == '"':
                char_s = "'\"'"
            
            else:
                char_s = '"\'"'

            return None, IllegalCharException( f'{char_s} expected', self.pos )

        self.advance()

        return Token( Constants.TT_STRING, s ).set_pos( start_pos, self.pos ), None

