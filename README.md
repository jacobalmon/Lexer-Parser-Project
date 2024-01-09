Lexer & Parser for TinyPie with GUI

Lexer & Parser for TinyPie (language we created) with Graphical User Interface that allows users to process code for our language.

Introduction:

Our project allows users to process code for our language. TinyPie is a simple language that does math for integers and floating points, conditional statements, and print statements.  The language is very similar to C++ for syntax. This project is done in Python. The Lexer was built using regex to find tokens within the source code using the module 're'. The Parser was built using a left-derivation algorithm based off our BNF grammar.

Our BNF Grammar is:

      math_exp -> key id = math
      math -> multi + multi
      multi -> float * multi | int * multi | float | int
      
      if_exp -> if(comparison_exp):
      comparison_exp -> id > id
      
      print_exp -> print("str_literal")
      
The Graphical User Interface was built using the module 'tkinter', the GUI allows the user to input code and when the 'submit line' is clicked, the interface outputs the tokens, the parse tree explanation, and the parse tree itself pops up as well with a vertical scrollbar. Although the parse trees are shown in tkinter, the implementation required us to use two helper classes we developed and a library 'anytree' to get it working. This project gives a better understanding of how a Compiler works as we do two of the processes for it.

Getting Started:

Download the source code and click run in whatever code editor you use. Enter whatever code you want that works with our grammar, the grammar is mentioned above in the Introduction of this document and is also commented on within the source code.

Prerequisites:

Code Editor of your Choice

Python 3 
            https://www.python.org/

AnyTree 
            'pip install anytree'

Usage:

We have a video and screenshots in our report demonstrating how it works.

Acknowledgments

Natalie Pedroza (Student of Computer Science)

Hannah Gonzalez (B.S. Mathematics of Education)
