class Exception:
    def __init__( self, name, desc, start_pos, end_pos=None ):
        self.name = name 
        self.desc = desc
        self.start_pos = start_pos 

        if end_pos == None and start_pos != None:
            end_pos = start_pos.copy()
            end_pos.advance()
            self.end_pos = end_pos
        
        else:
            self.end_pos = end_pos 
    
    def __repr__( self ):
        res = f'{self.name} : {self.desc}\n'
        if self.start_pos != None:
            res += f'Line {self.start_pos.ln + 1}, Col {self.start_pos.coln + 1}'

        return res
    

class Error:
    def __init__( self, name, desc, start_pos, end_pos=None ):
        self.name = name 
        self.desc = desc
        self.start_pos = start_pos 
        self.end_pos = end_pos 
    
    def __repr__( self ):
        res = f'{self.name} : {self.desc}\n'
        res += f'Line {self.start_pos.ln + 1}, Col {self.start_pos.coln + 1}'

        return res


class IllegalCharException( Exception ):
    def __init__( self, desc, start_pos, end_pos=None ):
        super().__init__( 'Illegal Character', desc, start_pos, end_pos )


class RuntimeException( Exception ):
    def __init__( self, desc, start_pos, end_pos=None ):
        super().__init__( 'Runtime Exception', desc, start_pos, end_pos )


class SyntaxError( Error ):
    def __init__( self, desc, start_pos, end_pos=None ):
        super().__init__( 'Syntax Error', desc, start_pos, end_pos )


class NameNotFoundError( Error ):
    def __init__( self, desc, start_pos, end_pos=None ):
        super().__init__( 'Name Error', desc, start_pos, end_pos )