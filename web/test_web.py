import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
if str(WEB_DIR) not in sys.path:
    sys.path.insert(0, str(WEB_DIR))

from app import analyze_source


def test_professor_example_service():
    data = analyze_source('printf("This is an example");\nint a = 10;')
    assert data["total_tokens"] == 10
    assert data["total_errors"] == 0


def test_lexical_error_recovery_service():
    data = analyze_source("int a = 10 @ 5;")
    assert data["total_tokens"] == 6
    assert data["total_errors"] == 1
    assert data["errors"][0]["lexeme"] == "@"


def test_http_endpoints():
    process = subprocess.Popen(
        [sys.executable, str(WEB_DIR / "app.py")],
        cwd=WEB_DIR.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 5
        while True:
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000/", timeout=1) as response:
                    html = response.read()
                    assert response.status == 200
                    assert b"Lexical Analyzer" in html
                    break
            except Exception:
                if time.time() > deadline:
                    raise
                time.sleep(0.1)

        with urllib.request.urlopen("http://127.0.0.1:5000/static/img/unam.png", timeout=2) as response:
            assert response.status == 200 and len(response.read()) > 0
        with urllib.request.urlopen("http://127.0.0.1:5000/static/img/fi.png", timeout=2) as response:
            assert response.status == 200 and len(response.read()) > 0

        request = urllib.request.Request(
            "http://127.0.0.1:5000/analyze",
            data=json.dumps({"source": 'printf("This is an example");\nint a = 10;'}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            data = json.loads(response.read().decode("utf-8"))
            assert data["total_tokens"] == 10
            assert data["total_errors"] == 0
    finally:
        process.terminate()
        process.wait(timeout=5)
