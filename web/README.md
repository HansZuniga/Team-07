# Team 07 Lexical Analyzer — Web Interface

This web interface calls the **original Team 07 Python lexer** located at:

`mx/unam/fi/compilers/g5/07/src/main/lexer.py`

It does not reimplement the lexer in JavaScript and never executes submitted source code.
The web server uses only Python's standard library, so no additional web framework is required.

## Run locally

From the project root:

```bash
python web/app.py
```

Then open:

`http://127.0.0.1:5000`

On Windows you can also double-click:

`run_web.bat`

## Run tests

Original lexer suite:

```bash
python -m pytest mx/unam/fi/compilers/g5/07/tests
```

Web integration tests:

```bash
python -m pytest web/test_web.py
```
