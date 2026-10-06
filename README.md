# Team 07 - Lexical Analyzer

Compilers Project  
Faculty of Engineering  
National Autonomous University of Mexico

## Team 07

| Team Member | Role |
|---|---|
| Parra Bello Carlos Enrique | Developer |
| Bojórquez Covarrubias Evans Martin | Writing |
| Arzate Ríos Adrian Axel | Presenter |
| Yáñez Barajas Brandon | Model Designer |
| Zúñiga García Hans David | Manager |

## Objective

Develop a lexical analyzer capable of receiving a string or a source code file as input, identifying the lexemes present in the input, and classifying them into tokens.

The program must display the recognized tokens and the total number of tokens found.

## Programming Language

Python 3

## Token Categories

The lexical analyzer recognizes the following token categories:

- Keywords
- Identifiers
- Operators
- Constants
- Literals
- Punctuation

Whitespace, tabs, and line breaks are not considered tokens.

Unrecognized characters are reported as lexical errors.

## Input

The lexer can receive:

1. A text string.
2. A source code file.

## Output

Each recognized token displays:

- Token type
- Lexeme
- Line
- Column

At the end of the analysis, the program displays the total number of recognized tokens.

## Example

Input:

```c
printf("This is an example");
int a = 10;
```

Expected token categories:

```text
IDENTIFIER
PUNCTUATION
LITERAL
PUNCTUATION
PUNCTUATION
KEYWORD
IDENTIFIER
OPERATOR
CONSTANT
PUNCTUATION
```

```text
Total of tokens: 10
```

## Project Structure

```text
Team-07/
├── docs/
├── mx/
│   └── unam/
│       └── fi/
│           └── compilers/
│               └── g5/
│                   └── 07/
│                       ├── examples/
│                       ├── resources/
│                       ├── src/main/
│                       ├── tests/
│                       └── README.md
├── .gitignore
├── README.md
└── requirements.txt
```

## Main Implementation

The lexer implementation is located in:

```text
mx/unam/fi/compilers/g5/07/src/main/
```

The project includes:

- Lexical analysis using regular expressions.
- Token classification.
- Keyword and identifier differentiation.
- Lexical error detection and recovery.
- String and file input.
- Line and column tracking.
- Token counting.
- Automated tests.

## Theoretical Documentation

The `docs/` folder contains the theoretical material used during the project, including:

- Token specification and regular expressions.
- NFA and DFA models.
- Context-Free Grammar (CFG).
- Left factoring.
- Technical report.

The final technical report is:

```text
docs/07-Compilers-Lexer.pdf
```

## Restrictions

- FLEX was not used.
- The lexical analyzer was implemented in Python.
- The project repository is public.
- The implementation follows the lexical analysis concepts studied during the course.

## Delivery Date

October 6, 2026
