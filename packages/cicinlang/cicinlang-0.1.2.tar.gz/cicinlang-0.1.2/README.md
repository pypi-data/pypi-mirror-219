# Cicinlang

Welcome to the Cicinlang repo. Cicinlang is a toy programming language created using Python. It is a general-purpose, procedural, interpreted language that includes support for loops, conditional statements, variables and functions (including partial support for anonymous functions).

This documentation serves as a guide on the basics of Cicinlang syntax.

## How To Use

First, install cicinlang using pip:

``` 
pip install cicinlang
```

Then, invoke the cicinlang script with the path of the file you want to execute:

```
cicinlang <path_to_file>
```

## Arithmetic and Logical Expressions

Cicinlang includes support for the following arithmetic operations:

- Addition (including unary +)
- Subraction (including unary -) 
- Multiplication ( * )
- Division ( / )
- Exponentiation ( ^ )
- Parentheses ( '(' , ')' )

The following logical operations are also supported:

- ASSIGNMENT ( = )
- OR ( or )
- AND ( and )
- NOT ( not )
- EQUALS ( == )
- NOT EQUALS ( != )
- GREATER THAN ( > )
- GREATER THAN OR EQUAL TO ( >= )
- LESS THAN ( < )
- LESS THAN OR EQUAL TO ( <= )

In Cicinlang, 0, 0.0 and "" represent False, and all other strings and numbers represent True.

The operator precedence of Cicinlang is as follows:

| Position | Operations |
| ----- | ----- |
| 1 | Function Calls, not, Unary +/-, () |
| 2 | ^ |
| 3 | * , / |
| 4 | <, <= |
| 5 | >, >= |
| 6 | ==, != | 
| 7 | and |
| 8 | or |
| 9 | = |

A few examples or arithmetic and logical expressions:

```
# Evaluated as  ( 1 + ( 2 * 3 ) - ( 4 ^ 5 ) ) or ( 0 <= 5 )
1 + 2 * 3 - ( 4 ^ 5 ) or 0 <= 5;

# Evaluated as ( ( 1 / 2 ) / 3 ) and ( not ( 6 or ( 7 != 8 ) ) )
1 / 2 / 3 and not 6 or 7 != 8;
```



## Variables

To declare and initialize a variable, use the 'var' keyword. To use an existing variable, just reference its name. To re-define a variable, simply define it without the 'var' keyword.

```
# Declaring and initializing
var a = 5;
var b = "hello github";
var c = ( a, b ) => { return a + b; }

# Referencing
print( str( a ) + b );

# Re-defining
a = 7.1; 
b = 8;
```

Note: Variables in Cicinlang are dynamically typed. This means a variable storing a string can be redefined to store a number.

In Cicinlang, variable assignment statements are expressions that return the assigned value.

```
var c = 10;
c = var a = 7;

# After the second statement, the value of c is updated to 7, and a new variable a is created with value 7
```

## Data Types

Cicinlang supports the following data types:

- Number ( integer and floats )
- String
- None 

One thing to note: None cannot be explicity defined. A variable can be set to None only if it is set to a function output and the function returns nothing. 

```
var c = () { print( 5 ); } # This function returns nothing

var d = c(); # The value of d will be None
```

## Strings

Cicinlang includes support for strings. They can be single-quoted or double quoted.

```
var s1 = 'Single quoted string';
var s2 = "Double quoted string";
```

Strings support the following operations:

- Binary '+' ( Causes concatenation )
- not 
- and 
- or

An empty string (i.e. a string with 0 characters) is a false-y value in Cicinlang

```
var gg = "hello" + " world"; # gg will be "hello world"
var gg2 = not ""; # gg2 will be 1
var gg3 = "" and "hello"; # gg3 will be 0
```

For the logical AND and logical OR operations, strings and numbers can be combined. 

```
var gg4 = "hello" and 5; # gg4 will be 1 since both "hello" and 5 are truth-ey values
```

## If-Statements

If-statements in Cicinlang are written as follows:

```
var level = 6;

if ( level < 7 ) {
    print( "Level is low." );
}

elif ( level < 10 ) {
    print( "Level is high." );
}

else {
    print( "Level is very high." );
}
```

The condition inside the if statement can be any valid expression that evaluates to a number. 

One quirk of if-statements in Cicinlang is that the else block has to be included even if there are no instructions inside it. For example, the following if-statement with no else-instructions has to be written like:

```
var else_test = 0;

if ( else_test ) {
    print( "Zero" );
}

else {} # This part has to be included even if empty
```

## For-loops

```
for( initialize_expr; condition_expr; update_expr ) {
    # Loop body
}
```

- 'initialize_expr' can be any valid expression within the language. For example, it can be a variable assignment, a whole if-chain, or any other valid statement.

- 'initialize_expr' can also be left empty. In that case, the syntax is as follows:

```
for( ; condition_expr; update_expr ) {
    # Loop body
}
```

- 'condition_expr' HAS to evaluate to a value. For example, it can be:
  - Arithmetic or logical expressions with strings and numbers
  - Variable assignments

-  The for-loop will continue as long as the condition_node evaluates to 0

- Like 'initialize_expr', 'update_expr' can be any valid expression inside the language

#### Example for-loop

```
for ( var i = 0; i < 5; i = i + 1 ) {
    print( "Current value of i:" );
    print( i );
}
```

As of July 2023, Cicinlang does not include support for while loops. 

## Functions

Functions are defined as follows:

```
var get_sum = ( val1, val2 ) {
    return val1 + val2;
}

var sum = get_sum( 4, 5 );

print( sum ); # Prints 9
```

- Unlike other statements in Cicinlang, variable assignment statements that defined functions don't have to end with a semicolon

- Fucntions can have 0 or more arguments passed into them

- Functions can also be returned by other functions:

```
var ret_func = () {
    return ( a, b ) { return a + b; }
}

var c = ret_func();

print( c( 1, 2 ) ); # Prints 3
```

- Before calling a function, it has to be put inside a variable first:

``` 
# () { return ( a ) { print( a ); } }()( 23 ); # THIS IS NOT VALID 

var func1 = () { return () { ( a ) { print( a ); } } }

# func1()( 23 ); # THIS IS NOT VALID

# This is valid
var e = func1();
e( 5 );
```

## Comments

```
# You can write comments by typing text after a hashtag
# Multi-line comments are not supported yet

var z = 10; # You can also write comments like this
```

## Print Statements

```
print( 5 ); # 5
print( 10 + 5 ); # 15
print( "a" + " cat" ); # a cat
print( 0 or "a" ); # 1
```

- Prints a statement and moves the cursor to the next line ( keeping the cursor in the same line is not currently supported )

- Functions cannot be printed unless they are stringified ( discussed later )

## Stringify Statements

- The below statement will throw and error: 

```
var a = 5 + " is an odd number.";
```

- Strings and numbers cannot be concatenated in Cicinlang. Hence, one might ask, "How can I join numbers and strings in statements to be able to print them?" Stringification is the answer:

```
var a = str( 5 ) + " is an odd number.";
```

- The above statement will not throw an error

- To stringify an expression, simply type str() and put the expression inside the parentheses.

## Input Statements

- Cicinlang supports taking user input. There are two relevant functions for user input: 
  - input_num( message ): First, 'message' is printed ( if given ). Then, a string input is taken from the user, and the program tries to convert it into a number. If it cannot do so, Cicinlang throws an error. The expression then evaluates to that number.

  - input_str( message ): First, 'message' is printed ( if given ). Then, a string input is taken from the user. The expression then evaluates to that string.

```
var name = input_str( "Enter your name: " );
var age = input_num( "Enter your age: " );

print( name + " is " + str( age ) + " years old." );
```

## Known Issues

- When errors are thrown, the line and column numbers might not always match the exact spot of the error

- In some cases, Python exceptions might be thrown instead of Cicinlang exceptions. This might be since those Python exceptions were not caught, or because there was a flaw with the implementation of the lexer, parser, or interpreter