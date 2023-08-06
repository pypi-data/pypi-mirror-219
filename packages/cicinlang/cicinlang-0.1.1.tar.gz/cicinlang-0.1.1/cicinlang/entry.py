#!/usr/bin/env python3

import sys 
import errno

from cicinlang.cicinlang import run 

def main():
    if len( sys.argv ) != 2:
        print( "Usage: cicinlang <path_to_file>" )
        return 

    path = sys.argv[1]

    try:
        with open( path, "r" ) as f:
            statement = f.read()
        
        try: 
            _, error = run( '<stdin>', statement )

        except KeyboardInterrupt:
            pass 

        else:
            if error: print( error )
    
    except IOError as x:
        if x.errno == errno.ENOENT:
            print( f"Error: {path} does not exist" )
        
        elif x.errno == errno.EISDIR:
            print( f"Error: {path} is a directory" )

        elif x.errno == errno.EACCES:
            print( f"Error: You don't have permissions to open {path}" )

        else:
            print( "Unknown Error. Please try again." )
            return 
    
    except: 
        print( "Unknown Error. Please try again." )
        return 

if __name__ == '__main__':
    main()