from cicinlang.utils import Constants, Context, SymbolTable
from cicinlang.errors import RuntimeException, NameNotFoundError

class Number:
    def __init__( self, value ):
        self.value = value 


class String:
    def __init__( self, value ):
        self.value = value 


class Function:
    def __init__( self, args, nodes ):
        self.args = args 
        self.nodes = nodes

class ReturnValue:
    def __init__( self, payload ):
        self.payload = payload


class NoneValue:
    def __init__( self ):
        self.value = None 


class Interpreter:   
    def interpret( self, ast_list, context ):
        for ast in ast_list:
            res, error = self.visit( ast, context ) 

            if error: return None, error

            if type( res ).__name__ == 'ReturnValue':
                return res, None 
        
        return NoneValue(), None 

    def visit( self, root, context ):
        type_name = type( root ).__name__ 

        if type_name == 'BinOpNode':
            left, error = self.visit( root.left_node, context )

            if error: return None, error 

            l_type = type( left ).__name__

            if l_type == 'ReturnValue':
                left = left.payload

            tok = root.tok

            right, error = self.visit( root.right_node, context )

            if error: return None, error

            r_type = type( right ).__name__

            if r_type == 'ReturnValue':
                right = right.payload

            is_func = l_type == 'Function' or r_type == 'Function'

            diff_types_wo_and_or_ee_ne = ( l_type != r_type ) and ( tok.type not in [ Constants.TT_KEYWORD, Constants.TT_EE, Constants.TT_NE ] )

            str_and_not_add_and_or = l_type == 'String' and tok.type not in [ Constants.TT_PLUS, Constants.TT_EE, Constants.TT_NE, Constants.TT_KEYWORD ]

            if is_func or diff_types_wo_and_or_ee_ne or str_and_not_add_and_or:
                return None, RuntimeException( f"Unsupported binary operation '{tok.value}' on types: '{l_type}' and '{r_type}'", root.start_pos, root.end_pos )
            
            return self.bin_op( left, tok, right )

        elif type_name == 'UnOpNode':
            res, error = self.interpret( root.node, context )

            if error: return None, error 

            res_type = type( res ).__name__

            if res_type == 'ReturnValue':
                res = res.payload

            is_func = res_type == 'Function'

            str_and_not_not = res_type == 'String' and root.tok.value != 'not'

            if is_func or str_and_not_not:
                return None, RuntimeException( f"Unsupported unary operator '{root.tok.value}' on type '{res_type}'", root.start_pos, root.end_pos )

            tok = root.tok 

            if tok.type == Constants.TT_PLUS: return Number( res.value ), None 

            elif tok.type == Constants.TT_KEYWORD and tok.value == 'not': return ( 0 if res.value else 1 ), None 

            else: return Number( -1 * num.value ), None 
        
        elif type_name == 'NumberNode':
            return Number( root.tok.value ), None 
        
        elif type_name == 'StringNode':
            return String( root.tok.value ), None 

        elif type_name == 'VarAssignNode':
            val, error = self.visit( root.var_value_node, context )

            if error: return None, error 

            if type( val ).__name__ == 'ReturnValue':
                val = val.payload

            tok = root.var_name_token.value
            tok_val = context.symbol_table.get_value( tok )
            start_pos = root.var_name_token.start_pos
            end_pos = root.var_name_token.end_pos

            if root.assign_type == Constants.AT_OLD and tok_val == None:
                return None, NameNotFoundError( f"'{tok}' not found", start_pos, end_pos )

            elif root.assign_type == Constants.AT_NEW and tok_val != None:
                return None, NameNotFoundError( f"'{tok}' is already declared.", start_pos, end_pos )

            context.symbol_table.set_value( tok, val )

            return val, None 

        elif type_name == 'VarAccessNode':
            value = context.symbol_table.get_value( root.var_name_token.value )
            
            if value == None:
                return None, NameNotFoundError( f"'{root.var_name_token.value}' not found", root.var_name_token.start_pos, root.var_name_token.end_pos )

            return value, None 

        elif type_name == 'IfNode':
            res, error = self.visit( root.if_condition_node, context )

            if error: return None, error 

            if type( res ).__name__ == 'ReturnValue':
                res = res.payload

            if type( res ).__name__ != 'Number':
                return None, RuntimeException( f"Condition value for if statement can only be Number, got {type( res ).__name__}", root.if_condition_node.start_pos, root.if_condition_node.end_pos )
            
            cond_val = res.value 

            if cond_val == 1:
                res, error = self.interpret( root.if_body_node_list, context )

                if error: return None, error 
                
                return res, None 

            for elif_cond_node, elif_body_node_list in zip( root.elif_condition_node_list, root.elif_body_node_lists ):
                res, error = self.visit( elif_cond_node )

                if error: return None, error 

                if type( res ).__name__ == 'ReturnValue':
                    res = res.payload

                if type( res ).__name__ != 'Number':
                    return None, RuntimeException( f"Condition value for if statement can only be Number, got {type( res ).__name__}", root.if_condition_node.start_pos, root.if_condition_node.end_pos )
                
                cond_val = res.value 

                if cond_val == 1:
                    res, error = self.interpret( elif_body_node_list, context )

                    if error: return None, error 

                    return res, None
            
            res, error = self.interpret( root.else_body_node_list, context )

            if error: return None, error 
            
            return res, None
          
        elif type_name == 'ForNode':
            if root.init_node != None:
                _, error = self.visit( root.init_node, context )

                if error: return None, error 

            cond_res, error = self.visit( root.cond_node, context )

            if error: return None, error 

            if type( cond_res ).__name__ == 'ReturnValue':
                cond_res = cond_res.payload

            cond_res_type = type( cond_res ).__name__

            if cond_res_type != "Number":
                return None, RuntimeException( f"Output of condition statement in for loop should be number, got {cond_res_type}", root.cond_node.start_pos, root.cond_node.end_pos )

            cond_val = cond_res.value

            while cond_val == 1:
                res, error = self.interpret( root.body_node_list, context )

                if error: return error 

                if type( res ).__name__ == 'ReturnValue':
                    return res, None 
                
                _, error = self.visit( root.update_node, context )

                if error: return None, error 

                cond_res, error = self.visit( root.cond_node, context )

                if error: return None, error 

                if type( cond_res ).__name__ == 'ReturnValue':
                    cond_res = cond_res.payload

                cond_res_type = type( cond_res ).__name__

                if cond_res_type != "Number":
                    return None, RuntimeException( f"Output of condition statement in for loop should be number, got {cond_res_type}", root.cond_node.start_pos, root.cond_node.end_pos )

                cond_val = cond_res.value
            
            return NoneValue(), None 

        elif type_name == 'FunctionDefNode':
            return Function( root.func_arg_toks_list, root.func_body_nodes_list ), None 

        elif type_name == 'FunctionCallNode':
            func_name = root.func_name_tok.value

            func = context.symbol_table.get_value( func_name )

            if func == None:
                return None, NameNotFoundError( f"{func_name} not found", root.func_name_tok.start_pos, root.func_name_tok.end_pos )
            
            if type( func ).__name__ != 'Function':
                return None, RuntimeException( f"Cannot invoke function call on type { type( func ).__name__ }", root.func_name_tok.start_pos, root.func_name_tok.end_pos )

            child_context = Context( func_name, context, root.func_name_tok.start_pos )
            child_symbol_table = SymbolTable( child_context )
            child_context.set_symbol_table( child_symbol_table )

            n_params = len( func.args )
            n_args = len( root.func_arg_nodes_list )

            if n_params != n_args:
                return None, RuntimeException( f"Expected {n_params} arguments, got {n_args}", root.start_pos, root.end_pos )

            for param_tok, node in zip( func.args, root.func_arg_nodes_list ):
                param_name = param_tok.value
                res, error = self.visit( node, context )

                if error: return None, error 

                if type( res ).__name__ == 'ReturnValue':
                    res = res.payload

                child_context.symbol_table.set_value( param_name, res )
            
            res, error = self.interpret( func.nodes, child_context )

            if error: return None, error 

            return res, None 

        elif type_name == 'PrintNode':
            res, error = self.visit( root.node, context )

            if error: return None, error 

            if type( res ).__name__ == 'ReturnValue':
                res = res.payload

            if type( res ).__name__ == 'Function':
                return None, RuntimeException( "Cannot print functions", root.node.start_pos, root.node.end_pos )

            print( res.value )

            return NoneValue(), None 
        
        elif type_name == 'InputNode':
            if root.node != None:
                res, error = self.visit( root.node, context )

                if error: return None, error 

                if type( res ).__name__ == 'ReturnValue':
                    res = res.payload

                if type( res ).__name__ == 'Function':
                    return None, RuntimeException( "Cannot print functions", root.node.start_pos, root.node.end_pos )
            
            else:
                res = None

            inp = input( res.value if res != None else '' )

            if root.inp_type == 'str':
                return String( inp ), None 
            
            elif root.inp_type == 'num':
                try: 
                    num = float( inp ) if '.' in inp else int( inp )

                except:
                    return None, RuntimeException( f"Could not convert '{inp}' to Number", root.start_pos, root.end_pos )

                else:
                    return Number( num ), None 

        elif type_name == 'ReturnNode':
            res, error = self.visit( root.node, context )

            if error: return None, error 

            if type( res ).__name__ == 'ReturnValue':
                return res, None 
            
            return ReturnValue( res ), None 

        elif type_name == 'StringifyNode':
            res, error = self.visit( root.node, context )

            if error: return None, error 

            if type( res ).__name__ == 'ReturnValue':
                res = res.payload
            
            if type( res ).__name__ == 'Function':
                return String( f'<Function object>' ), None 

            else: 
                return String( str( res.value ) ), None

        elif type_name == 'NoneType':
            pass

        else:
            return None, 'Interpreting Error'
    
    def bin_op( self, left, tok, right ):
        if tok.type == Constants.TT_PLUS: 
            if type( left ).__name__ == 'Number':
                return Number( left.value + right.value ), None 
            
            elif type( left ).__name__ == 'String':
                return String( left.value + right.value ), None 
            
        elif tok.type == Constants.TT_MINUS: return Number( left.value - right.value ), None 

        elif tok.type == Constants.TT_MUL: return Number( left.value * right.value ), None 

        elif tok.type == Constants.TT_EXP: return Number( left.value ** right.value ), None

        elif tok.type == Constants.TT_DIV:
            if right.value == 0: return None, RuntimeException( 'Division by 0', tok.start_pos )

            return Number( left.value / right.value ), None

        elif tok.type == Constants.TT_LT: return Number( 1 if left.value < right.value else 0 ), None 

        elif tok.type == Constants.TT_LTE: return Number( 1 if left.value <= right.value else 0 ), None 

        elif tok.type == Constants.TT_GT: return Number( 1 if left.value > right.value else 0 ), None

        elif tok.type == Constants.TT_GTE: return Number( 1 if left.value >= right.value else 0 ), None

        elif tok.type == Constants.TT_EE: return Number( 1 if left.value == right.value else 0 ), None

        elif tok.type == Constants.TT_NE: return Number( 1 if left.value != right.value else 0 ), None

        elif tok.type == Constants.TT_KEYWORD and tok.value == 'and': return Number( 1 if left.value and right.value else 0 ), None

        elif tok.type == Constants.TT_KEYWORD and tok.value == 'or': return Number( 1 if left.value or right.value else 0 ), None