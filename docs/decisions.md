# Design Decisions - Team 07

This document contains the main decisions taken during the development of the lexical analyzer for Team 07.

The purpose is to keep the theoretical model, implementation, report, and presentation consistent throughout the project.

---

## 1. Programming Language

The lexical analyzer will be developed in Python 3.

Python was selected because it allows the team to focus on the lexical analysis logic while working directly with strings, files, and regular expressions.

---

## 2. Project Scope

The main product of this project is a lexical analyzer.

The lexer will:

1. Receive source code as input.
2. Scan the input from left to right.
3. Identify lexemes.
4. Classify each lexeme into a token category.
5. Display the recognized tokens.
6. Count the total number of valid tokens.
7. Report lexical errors when an element cannot be recognized.

A complete parser will not be implemented as part of this delivery.

The grammar concepts studied in class will be used as theoretical support and for the CFG example required in the project.

---


## 3. Token Categories

The lexer will recognize the following token categories:

- `KEYWORD`
- `IDENTIFIER`
- `OPERATOR`
- `CONSTANT`
- `LITERAL`
- `PUNCTUATION`

Example:

```c
int result = 10;
```

## 4. Keywords and Identifiers

Keywords and identifiers can initially follow a similar lexical pattern.

For this reason, the lexer will first determine whether a lexeme follows the identifier pattern.

After that, it will check whether the lexeme belongs to the reserved-word list.

If it belongs to that list, it will be classified as `KEYWORD`.

Otherwise, it will remain classified as `IDENTIFIER`.
