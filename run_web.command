#!/bin/bash

cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required to run the Team 07 Lexical Analyzer."
    echo "Install Python 3 and try again."
    read -r -p "Press Enter to close..."
    exit 1
fi

echo "Team 07 Lexical Analyzer"
echo "Open http://127.0.0.1:5000 in your browser"
echo "Press Ctrl+C to stop the server."

(sleep 1; open "http://127.0.0.1:5000") &
python3 web/app.py
