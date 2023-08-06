from cicinlang.nodes import *
from cicinlang.utils import Constants, Token
from cicinlang.errors import SyntaxError

class Parser:
    def __init__( self, tokens ):
        self.tokens = tokens
        self.idx = -1
        self.advance()
    
    def advance( self ):
        self.idx += 1
        self.cur_tok = self.tokens[self.idx] if self.idx < len( self.tokens ) else None 
    
    def parse( self ):
        exprs = []

        while self.cur_tok.type != Constants.TT_EOF:
            head, error = self.expr()

            if error: return None, error 

            node_type = type( head ).__name__

            semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( head.var_value_node ).__name__ != 'FunctionDefNode' )

            if semicolon_required:
                if self.cur_tok.type != Constants.TT_SEMICOLON:
                    return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

            exprs.append( head )
        
        return exprs, None 

    def bin_op_term( self, parse_func, tok_val_func ):
        left, error = parse_func()

        if error: return None, error 

        while tok_val_func( self.cur_tok ):
            tok = self.cur_tok 
            self.advance()
            right, error = parse_func()

            if error: return None, error 
            
            left = BinOpNode( left, tok, right )
        
        return left, None 
    
    def expr( self, inside_func=False ):
        expr_head, error = self.void_expr( inside_func ) if self.cur_tok.value in [ 'for', 'if', 'print', 'return' ] else self.value_expr()

        if error: return None, error 

        return expr_head, None 

    def value_expr( self ):
        if self.cur_tok.value == 'var': 
            self.advance()

            name_tok = self.cur_tok 

            if name_tok.type != Constants.TT_IDENTIFIER:
                return None, SyntaxError( "Expected Identifier", self.cur_tok.start_pos, self.cur_tok.end_pos )
            
            self.advance()

            if self.cur_tok.type != Constants.TT_EQ:
                return None, SyntaxError( "Expected '='", self.cur_tok.start_pos, self.cur_tok.end_pos )
            
            self.advance()

            value_node, error = self.value_expr()

            if error: return None, error 

            return VarAssignNode( name_tok, value_node, Constants.AT_NEW ), None

        head, error = self.or_chain()

        if error: return None, error 

        if type( head ).__name__ == 'VarAccessNode' and self.cur_tok.type == Constants.TT_EQ:
            name_tok = head.var_name_token

            self.advance()

            value_node, error = self.value_expr()

            if error: return None, error 

            return VarAssignNode( name_tok, value_node, Constants.AT_OLD ), None
        
        return head, None 

    def void_expr( self, inside_func=False ):
        if self.cur_tok.value == 'for':
            for_head, error = self.for_loop( inside_func )

            if error: return None, error 

            return for_head, None 
        
        elif self.cur_tok.value == 'if':
            if_head, error = self.if_stmt( inside_func )

            if error: return None, error 

            return if_head, None 
        
        elif self.cur_tok.value == 'print':
            print_head, error = self.print_stmt()

            if error: return None, error 

            return print_head, None 
        
        elif self.cur_tok.value == 'return':
            if not inside_func: 
                return None, SyntaxError( "Return statements only allowed as standalone statements inside functions", self.cur_tok.start_pos, self.cur_tok.end_pos )
            
            self.advance()

            head, error = self.value_expr()

            if error: return None, error 

            return ReturnNode( head ), None 

    def or_chain( self ):
        return self.bin_op_term( self.or_operand, lambda x : x.value == 'or' )
    
    def or_operand( self ):
        return self.bin_op_term( self.and_operand, lambda x : x.value == 'and' )
    
    def and_operand( self ):
        return self.bin_op_term( self.ee_operand, lambda x : x.type in [ Constants.TT_EE, Constants.TT_NE ] )
    
    def ee_operand( self ):
        return self.bin_op_term( self.gt_operand, lambda x : x.type in [ Constants.TT_GT, Constants.TT_GTE ] )
    
    def gt_operand( self ):
        return self.bin_op_term( self.lt_operand, lambda x : x.type in [ Constants.TT_LT, Constants.TT_LTE ] )
    
    def lt_operand( self ):
        return self.bin_op_term( self.term, lambda x : x.type in [ Constants.TT_PLUS, Constants.TT_MINUS ] )
    
    def term( self ):
        return self.bin_op_term( self.factor, lambda x : x.type in [ Constants.TT_MUL, Constants.TT_DIV ] )
    
    def factor( self ):
        atoms = []

        head, error = self.atom()

        if error: return None, error 

        if type( head ).__name__ == 'FunctionDefNode': return head, None

        atoms.append( head )

        while self.cur_tok.type == Constants.TT_EXP:
            self.advance()

            head, error = self.atom()

            if error: return None, error 

            atoms.append( head )
        
        while len( atoms ) > 1:
            right = atoms.pop()
            left = atoms.pop()

            atoms.append( BinOpNode( left, Token( Constants.TT_EXP ), right ) )

        return atoms[0], None

    def atom( self ):
        if self.cur_tok.type in [ Constants.TT_INT, Constants.TT_FLOAT ]:
            tok = self.cur_tok 
            self.advance()

            return NumberNode( tok ), None 
        
        elif self.cur_tok.type == Constants.TT_STRING:
            tok = self.cur_tok
            self.advance()

            return StringNode( tok ), None

        elif self.cur_tok.type == Constants.TT_IDENTIFIER:
            tok = self.cur_tok 
            self.advance()

            if self.cur_tok.type != Constants.TT_LPAREN:
                return VarAccessNode( tok ), None 
            
            self.advance()

            func_arg_nodes_list = [] 

            while self.cur_tok.type != Constants.TT_RPAREN:
                head, error = self.value_expr()

                if error: return None, error 

                func_arg_nodes_list.append( head )

                if self.cur_tok.type == Constants.TT_COMMA:
                    self.advance()
                
                elif self.cur_tok.type != Constants.TT_RPAREN:
                    return None, SyntaxError( "Expected ',' or ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
            
            self.advance()

            return FunctionCallNode( tok, func_arg_nodes_list ), None
        
        elif self.cur_tok.type == Constants.TT_LPAREN:
            self.advance()

            if self.cur_tok.type == Constants.TT_RPAREN:
                func_arg_toks_list = []
                func_body_nodes_list = []

                self.advance()

                if self.cur_tok.type != Constants.TT_LBRACE:
                    return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                lbrace_tok = self.cur_tok 

                self.advance()

                while self.cur_tok.type != Constants.TT_RBRACE:
                    head, error = self.expr( True )

                    if error: return None, error 

                    node_type = type( head ).__name__

                    semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( head.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( head.node ).__name__ != 'FunctionDefNode' )

                    if semicolon_required:
                        if self.cur_tok.type != Constants.TT_SEMICOLON:
                            return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                        
                        self.advance()
                    
                    func_body_nodes_list.append( head )

                if len( func_body_nodes_list ) == 0:
                    return None, SyntaxError( "Functions with empty bodies are not supported", lbrace_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

                return FunctionDefNode( func_arg_toks_list, func_body_nodes_list ), None 

            head, error = self.value_expr()

            if error: return None, error 

            nt = type( head ).__name__

            if nt == 'VarAccessNode' and self.cur_tok.type == Constants.TT_COMMA:
                func_arg_toks_list = [ head.var_name_token ]

                self.advance()

                while self.cur_tok.type != Constants.TT_RPAREN:
                    head, error = self.value_expr()

                    if error: return None, error 

                    if type( head ).__name__ != 'VarAccessNode':
                        return None, SyntaxError( "Expected identifier", head.start_pos, head.end_pos )
                    
                    func_arg_toks_list.append( head.var_name_token )
                
                self.advance()

                if self.cur_tok.type != Constants.TT_LBRACE:
                    return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

                func_body_nodes_list = []

                while self.cur_tok.type != Constants.TT_RBRACE:
                    head, error = self.expr( True )

                    if error: return None, error

                    node_type = type( head ).__name__

                    semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( head.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( head.node ).__name__ != 'FunctionDefNode' )

                    if semicolon_required:
                        if self.cur_tok.type != Constants.TT_SEMICOLON:
                            return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                        
                        self.advance()
                    
                    func_body_nodes_list.append( head )

                if len( func_body_nodes_list ) == 0:
                    return None, SyntaxError( "Functions with empty bodies are not supported", lbrace_tok.start_pos, self.cur_tok.end_pos )

                self.advance()

                return FunctionDefNode( func_arg_toks_list, func_body_nodes_list ), None

            if self.cur_tok.type != Constants.TT_RPAREN:
                return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
            
            self.advance()

            func_arg_toks_list = [ head.var_name_token ]

            if nt != 'VarAccessNode' or self.cur_tok.type != Constants.TT_LBRACE:
                return head, None 
            
            self.advance()

            func_body_nodes_list = []

            while self.cur_tok.type != Constants.TT_RBRACE:
                head, error = self.expr( True )
                
                if error: return None, error

                node_type = type( head ).__name__

                semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( head.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( head.node ).__name__ != 'FunctionDefNode' )

                if semicolon_required:
                    if self.cur_tok.type != Constants.TT_SEMICOLON:
                        return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                    
                    self.advance()
                
                func_body_nodes_list.append( head )

            self.advance()

            return FunctionDefNode( func_arg_toks_list, func_body_nodes_list ), None
        
        elif self.cur_tok.type in [ Constants.TT_PLUS, Constants.TT_MINUS ] or self.cur_tok.value == 'not':
            tok = self.cur_tok

            self.advance()

            node, error = self.atom()

            if error: return None, error 

            return UnOpNode( tok, node ), None 

        elif self.cur_tok.value in [ 'input_str', 'input_num' ]:
            input_head, error = self.input_stmt()

            if error: return None, error 

            return input_head, None

        elif self.cur_tok.value == 'str':
            str_head, error = self.stringify_stmt()

            if error: return None, error 

            return str_head, None

        else:
            return None, SyntaxError( "Expected int, float, identifier, '(', '+', '-' or 'not'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
    def if_stmt( self, inside_func=False ):
        self.advance()

        if self.cur_tok.type != Constants.TT_LPAREN:
            return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if_condition_node, error = self.value_expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_RPAREN:
            return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if self.cur_tok.type != Constants.TT_LBRACE:
            return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if_body_node_list = []

        while self.cur_tok.type != Constants.TT_RBRACE:
            if_body_node, error = self.expr( inside_func )

            if error: return None, error 

            node_type = type( if_body_node ).__name__

            semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( if_body_node.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( if_body_node.node ).__name__ != 'FunctionDefNode' )

            if semicolon_required:
                if self.cur_tok.type != Constants.TT_SEMICOLON:
                    return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

            if_body_node_list.append( if_body_node )
        
        self.advance()

        elif_cond_node_list = []
        elif_body_node_lists = []

        while self.cur_tok.value == 'elif':
            self.advance()

            if self.cur_tok.type != Constants.TT_LPAREN:
                return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
            self.advance()

            elif_cond_node, error = self.value_expr()

            if error: return None, error 

            elif_cond_node_list.append( elif_cond_node )

            if self.cur_tok.type != Constants.TT_RPAREN:
                return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
            self.advance()

            if self.cur_tok.type != Constants.TT_LBRACE:
                return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
            self.advance()

            elif_body_node_list = []

            while self.cur_tok.type != Constants.TT_RBRACE:
                elif_body_node, error = self.expr( inside_func )

                if error: return None, error 

                node_type = type( elif_body_node ).__name__

                semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( elif_body_node.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( elif_body_node.node ).__name__ != 'FunctionDefNode' )

                if semicolon_required:
                    if self.cur_tok.type != Constants.TT_SEMICOLON:
                        return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                    
                    self.advance()

                elif_body_node_list.append( elif_body_node )
            
            self.advance()

            elif_body_node_lists.append( elif_body_node_list )

        if self.cur_tok.value != 'else':
            return None, SyntaxError( "Expected 'else'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if self.cur_tok.type != Constants.TT_LBRACE:
            return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )

        self.advance()

        else_body_node_list = []

        while self.cur_tok.type != Constants.TT_RBRACE:
            else_body_node, error = self.expr( inside_func )

            if error: return None, error 

            node_type = type( else_body_node ).__name__

            semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( else_body_node.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( else_body_node.node ).__name__ != 'FunctionDefNode' )

            if semicolon_required:
                if self.cur_tok.type != Constants.TT_SEMICOLON:
                    return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

            else_body_node_list.append( else_body_node )
        
        self.advance()

        return IfNode( if_condition_node, if_body_node_list, elif_cond_node_list, elif_body_node_lists, else_body_node_list ), None

    def for_loop( self, inside_func=False ):
        init_node = None 

        self.advance()

        if self.cur_tok.type != Constants.TT_LPAREN:
            return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if self.cur_tok.type != Constants.TT_SEMICOLON:
            init_node, error = self.expr()

            if error: return None, error 

        if self.cur_tok.type != Constants.TT_SEMICOLON:
            return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        cond_node, error = self.value_expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_SEMICOLON:
            return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        update_node, error = self.expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_RPAREN:
            return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if self.cur_tok.type != Constants.TT_LBRACE:
            return None, SyntaxError( "Expected '{'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        body_node_list = []

        while self.cur_tok.type != Constants.TT_RBRACE:
            head, error = self.expr( inside_func )

            if error: return None, error 

            node_type = type( head ).__name__

            semicolon_required = node_type not in [ "ForNode", "IfNode", "FunctionDefNode" ] and ( node_type != 'VarAssignNode' or type( head.var_value_node ).__name__ != 'FunctionDefNode' ) and ( node_type != 'ReturnNode' or type( head.node ).__name__ != 'FunctionDefNode' )

            if semicolon_required:
                if self.cur_tok.type != Constants.TT_SEMICOLON:
                    return None, SyntaxError( "Expected ';'", self.cur_tok.start_pos, self.cur_tok.end_pos )
                
                self.advance()

            body_node_list.append( head )
        
        self.advance()

        return ForNode( init_node, cond_node, update_node, body_node_list ), None

    def print_stmt( self ):
        self.advance()

        if self.cur_tok.type != Constants.TT_LPAREN:
            return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        head, error = self.value_expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_RPAREN:
            return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        return PrintNode( head ), None
    
    def input_stmt( self ):
        inp_type = 'str' if self.cur_tok.value == 'input_str' else 'num'
        self.advance()

        if self.cur_tok.type != Constants.TT_LPAREN:
            return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        if self.cur_tok.type == Constants.TT_RPAREN:
            self.advance()
            return InputNode( None, inp_type ), None

        head, error = self.value_expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_RPAREN:
            return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        return InputNode( head, inp_type ), None
    
    def stringify_stmt( self ): 
        self.advance()

        if self.cur_tok.type != Constants.TT_LPAREN:
            return None, SyntaxError( "Expected '('", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        head, error = self.value_expr()

        if error: return None, error 

        if self.cur_tok.type != Constants.TT_RPAREN:
            return None, SyntaxError( "Expected ')'", self.cur_tok.start_pos, self.cur_tok.end_pos )
        
        self.advance()

        return StringifyNode( head ), None
