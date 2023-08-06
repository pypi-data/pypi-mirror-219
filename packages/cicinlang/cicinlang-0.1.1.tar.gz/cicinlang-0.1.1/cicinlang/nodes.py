class NumberNode:
    def __init__( self, tok ):
        self.tok = tok 
        self.start_pos = tok.start_pos
        self.end_pos = tok.end_pos

    def __repr__( self ):
        return f'{self.tok}'
    

class StringNode:
    def __init__( self, tok ):
        self.tok = tok 
        self.start_pos = tok.start_pos
        self.end_pos = tok.end_pos

    def __repr__( self ):
        return f'{self.tok}'


class BinOpNode:
    def __init__( self, left_node, tok, right_node ):
        self.left_node = left_node
        self.tok = tok
        self.right_node = right_node
        self.start_pos = left_node.start_pos
        self.end_pos = right_node.end_pos

    def __repr__( self ):
        return f'( {self.left_node}, {self.tok}, {self.right_node} )'


class UnOpNode:
    def __init__( self, tok, node ):
        self.tok = tok 
        self.node = node 
        self.start_pos = tok.start_pos 
        self.end_pos = node.end_pos
    
    def __repr__( self ):
        return f'( {self.tok}, {self.node} )'
    

class VarAssignNode:
    def __init__( self, var_name_token, var_value_node, assign_type ):
        self.var_name_token = var_name_token  # This token is an IDENTIFIER token
        self.var_value_node = var_value_node  # This node will be an expression node
        self.start_pos = var_name_token.start_pos
        self.end_pos = var_value_node.end_pos
        self.assign_type = assign_type
    
    def __repr__( self ):
        return f'( {self.var_name_token.value} : {self.var_value_node} )'


class VarAccessNode:
    def __init__( self, var_name_token ):
        self.var_name_token = var_name_token 
        self.start_pos = var_name_token.start_pos
        self.end_pos = var_name_token.end_pos

    def __repr__( self ):
        return f'{self.var_name_token.value}'
    

class IfNode:
    def __init__( self, if_condition_node, if_body_node_list, elif_condition_node_list, elif_body_node_lists, else_body_node_list ):
        self.if_condition_node = if_condition_node
        self.if_body_node_list = if_body_node_list
        self.elif_condition_node_list = elif_condition_node_list
        self.elif_body_node_lists = elif_body_node_lists
        self.else_body_node_list = else_body_node_list
        self.start_pos = if_condition_node.start_pos if if_condition_node != None else None
        
        if len( else_body_node_list ) > 0:
            self.end_pos = else_body_node_list[-1].end_pos

        elif len( elif_condition_node_list ) > 0:
            if len( elif_body_node_lists[-1] ) > 0:
                self.end_pos = elif_body_node_lists[-1][-1].end_pos
                
            else:
                self.end_pos = elif_condition_node_list[-1].end_pos

        elif len( if_body_node_list ) > 0:
            self.end_pos = if_body_node_list[-1].end_pos
        
        else:
            self.end_pos = if_condition_node.end_pos if if_condition_node != None else None

    def __repr__( self ):
        return f'( IF: {self.if_condition_node}, {self.if_body_node_list}, ELIF: {self.elif_condition_node_list}, {self.elif_body_node_lists}, ELSE: {self.else_body_node_list} )'
    

class ForNode:
    def __init__( self, init_node, cond_node, update_node, body_node_list ):
        self.init_node = init_node  
        self.cond_node = cond_node 
        self.update_node = update_node 
        self.body_node_list = body_node_list
        self.start_pos = init_node.start_pos if init_node != None else cond_node.start_pos
        self.end_pos = body_node_list[-1].end_pos if len( body_node_list ) > 0 else update_node.end_pos

    def __repr__( self ):
        return f'( FOR: {self.init_node}, {self.cond_node}, {self.update_node}, {self.body_node_list} )'


class FunctionDefNode:
    def __init__( self, func_arg_toks_list, func_body_nodes_list ):
        self.func_arg_toks_list = func_arg_toks_list
        self.func_body_nodes_list = func_body_nodes_list
        self.start_pos = func_arg_toks_list[0].start_pos if len( func_arg_toks_list ) > 0 else func_body_nodes_list[0].start_pos
        self.end_pos = func_body_nodes_list[-1].end_pos
    
    def __repr__( self ):
        return f'( FUNC - ARGS:{self.func_arg_toks_list}, BODY:{self.func_body_nodes_list} )'


class FunctionCallNode:
    def __init__( self, func_name_tok, func_arg_nodes_list ):
        self.func_name_tok = func_name_tok
        self.func_arg_nodes_list = func_arg_nodes_list
        self.start_pos = func_name_tok.start_pos
        self.end_pos = func_arg_nodes_list[-1].end_pos if len( func_arg_nodes_list ) > 0 else func_name_tok.end_pos

    def __repr__( self ):
        return f'( CALLING FUNC "{self.func_name_tok.value}" WITH ARGS {self.func_arg_nodes_list} )'


class ReturnNode:
    def __init__( self, val_node ):
        self.node = val_node
        self.start_pos = val_node.start_pos
        self.end_pos = val_node.end_pos
    
    def __repr__( self ):
        return f'( RETURN {self.node} )'


class PrintNode:
    def __init__( self, node ):
        self.node = node 
        self.start_pos = node.start_pos
        self.end_pos = node.end_pos
    
    def __repr__( self ):
        return f'( PRINT: {self.node} )'
    

class InputNode:
    def __init__( self, node, inp_type ):
        self.node = node 
        self.inp_type = inp_type
        self.start_pos = node.start_pos if node != None else None
        self.end_pos = node.end_pos if node != None else None 
    
    def __repr__( self ):
        return f'( INPUT({self.inp_type}) - MSG: {self.node} )'


class StringifyNode:
    def __init__( self, node ):
        self.node = node
        self.start_pos = node.start_pos 
        self.end_pos = node.end_pos