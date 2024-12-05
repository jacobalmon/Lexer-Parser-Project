# Lexer & Parser for TinyPie

## Introduction
This project is a Lexer and Parser built for a custom language called TinyPie. It provides a graphical interface using `tkinter` to tokenize and parse input code, displaying the results and parse trees in real-time. The system follows a simplified grammar and uses `anytree` to visualize parse trees.

## Table of Contents
- [Features](#features)
- [Grammar Rules](#grammar-rules)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contributors](#contributors)

## Features
- **Lexical Analysis**: Tokenizes input code into keywords, identifiers, operators, separators, and literals.
- **Syntax Parsing**: Builds and visualizes parse trees based on predefined grammar.
- **Real-time Processing**: Processes input line-by-line with on-screen updates.
- **Tree Visualization**: Displays the generated parse tree for each line of code.

## Grammar Rules
The project supports the following simplified grammar:
- **Mathematical Expressions**:
    ```plaintext
    math_exp -> key id = math
    math -> multi + multi
    multi -> float * multi | int * multi | float | int
    ```
- **Conditional Statements**:
    ```plaintext
    if_exp -> if(comparison_exp):
    comparison_exp -> id > id
    ```
- **Print Statements**:
    ```plaintext
    print_exp -> print("str_literal")
    ```

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/tinypie-lexer-parser.git
    ```
2. Install the required Python packages:
    ```bash
    pip install tkinter anytree
    ```

## Usage
1. Run the application:
    ```bash
    python your_script_name.py
    ```
2. Enter source code in the **Source Code** text box.
3. Click **Next Line** to process each line and view tokens.
4. View the generated parse tree in the **Tree Visualization** section.
5. Click **EXIT** to close the application.

## Dependencies
- **Python 3.x**
- **tkinter**: For the GUI interface.
- **anytree**: For parse tree visualization.
- **re**: For regular expression-based tokenization.

## Configuration
No special configuration is needed. You can modify the grammar or tokenization logic by editing the `cutOneLineTokens` function and parser methods.

## Contributors
Hannah Gonzalez

Natalie Pedroza
