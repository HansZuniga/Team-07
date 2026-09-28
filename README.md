Proyecto de la materia de Compiladores  
Facultad de Ingeniería  
Universidad Nacional Autónoma de México

## Equipo 7

| Integrante | Rol |
|---|---|
| Parra Bello Carlos Enrique | Developer |
| Bojórquez Covarrubias Evans Martin | Writing |
| Arzate Ríos Adrian Axel | Presenter |
| Yáñez Barajas Brandon | Model Designer |
| Zúñiga García Hans David | Manager |

## Objetivo

Desarrollar un analizador léxico capaz de recibir una cadena o un archivo
de entrada, identificar los lexemas presentes y clasificarlos en tokens.

El programa deberá mostrar los tokens reconocidos y el número total de
tokens encontrados.

## Lenguaje de programación

Python 3

## Tokens contemplados

El analizador reconocerá inicialmente las siguientes categorías:

- Keywords
- Identifiers
- Operators
- Constants
- Literals
- Punctuation

Los espacios en blanco, tabulaciones y saltos de línea no serán considerados tokens.

Los caracteres no reconocidos se reportarán como errores léxicos.

## Entrada

El lexer podrá recibir:

1. Una cadena de texto.
2. Un archivo de código.

## Salida

Cada token identificado deberá mostrar:

- Tipo de token.
- Lexema.
- Línea.
- Columna.

Además, al final se mostrará el número total de tokens encontrados.

### Ejemplo

Entrada:

```c
printf("This is an example");
int a = 10;
