# unam.fi.compilers.g5.07 — Lexer

Implementación del analizador léxico (lexer) del Equipo 07.

## Estructura

```
07/
├── resources/
│   └── keywords.txt       # Palabras reservadas: print, int, return, if, else
├── src/main/
│   ├── lexer.py            # Clase Lexer: núcleo del análisis léxico
│   └── main.py              # Punto de entrada / CLI
├── examples/
│   └── example_profesor.c  # 
└── tests/
    └── test_lexer.py        # Pruebas unitarias (pytest)
```

## Uso

Desde `src/main/`:

```bash
# Analiza el ejemplo del profesor (por defecto)
python main.py

# Analiza un archivo específico
python main.py --file ../../examples/example_profesor.c

# Analiza una cadena literal
python main.py --text "int a = 10;"
```

## Pruebas

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
pytest mx/unam/fi/compilers/g5/07/tests
```

## Categorías de tokens

| Categoría    | Patrón                           |
|--------------|-----------------------------------|
| KEYWORD      | `print \| int \| return \| if \| else` |
| IDENTIFIER   | `[A-Za-z_][A-Za-z0-9_]*`          |
| CONSTANT     | `[0-9]+(?:\.[0-9]+)?`             |
| LITERAL      | `"[^"\r\n]*"`                     |
| OPERATOR     | `==\|!=\|<=\|>=\|[=+*/<>-]`       |
| PUNCTUATION  | `[(){};,]`                        |

Ver `docs/Especificacion_Tokens.pdf` para el detalle completo de la especificación,
reglas de prioridad y manejo de errores léxicos.
