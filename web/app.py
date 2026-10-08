from __future__ import annotations

import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

WEB_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = WEB_DIR.parent
LEXER_DIR = PROJECT_ROOT / "mx" / "unam" / "fi" / "compilers" / "g5" / "07" / "src" / "main"
KEYWORDS_PATH = PROJECT_ROOT / "mx" / "unam" / "fi" / "compilers" / "g5" / "07" / "resources" / "keywords.txt"
INDEX_FILE = WEB_DIR / "templates" / "index.html"
STATIC_DIR = WEB_DIR / "static"
MAX_SOURCE_LENGTH = 50_000
MAX_REQUEST_BYTES = 64 * 1024

if str(LEXER_DIR) not in sys.path:
    sys.path.insert(0, str(LEXER_DIR))

from lexer import Lexer  # noqa: E402


def analyze_source(source: str) -> dict:
    """Run the original Team 07 lexer and return JSON-serializable results."""
    if not isinstance(source, str):
        raise TypeError("Source must be text.")
    if len(source) > MAX_SOURCE_LENGTH:
        raise ValueError(f"Input is too large. Maximum length is {MAX_SOURCE_LENGTH:,} characters.")

    lexer = Lexer(keywords_path=KEYWORDS_PATH)
    lexer.tokenize(source)
    return {
        "ok": True,
        "tokens": [token.as_dict() for token in lexer.tokens],
        "errors": [error.as_dict() for error in lexer.errors],
        "total_tokens": lexer.get_total_tokens(),
        "total_errors": len(lexer.errors),
    }


class LexerWebHandler(BaseHTTPRequestHandler):
    server_version = "Team07LexerWeb/1.0"

    def log_message(self, format, *args):  # noqa: A003
        # Keep console output concise while still showing requests.
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def _send_bytes(self, data: bytes, status: int = 200, content_type: str = "application/octet-stream"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: dict, status: int = 200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(data, status, "application/json; charset=utf-8")

    def do_GET(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._serve_file(INDEX_FILE, "text/html; charset=utf-8")
            return

        if path.startswith("/static/"):
            relative = path[len("/static/"):]
            candidate = (STATIC_DIR / relative).resolve()
            static_root = STATIC_DIR.resolve()
            try:
                candidate.relative_to(static_root)
            except ValueError:
                self._send_json({"ok": False, "message": "Not found."}, 404)
                return
            self._serve_file(candidate)
            return

        self._send_json({"ok": False, "message": "Not found."}, 404)

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        if path != "/analyze":
            self._send_json({"ok": False, "message": "Not found."}, 404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            self._send_json({"ok": False, "message": "Invalid or oversized request."}, 413)
            return

        try:
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                raise TypeError("Invalid request body.")
            source = payload.get("source", "")
            result = analyze_source(source)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
            self._send_json({"ok": False, "message": str(exc) or "Invalid request body."}, 400)
            return
        except ValueError as exc:
            self._send_json({"ok": False, "message": str(exc)}, 413)
            return
        except Exception:
            self._send_json({"ok": False, "message": "The analyzer could not process the request."}, 500)
            return

        self._send_json(result)

    def _serve_file(self, path: Path, forced_type: str | None = None):
        if not path.is_file():
            self._send_json({"ok": False, "message": "Not found."}, 404)
            return
        data = path.read_bytes()
        content_type = forced_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") and "charset" not in content_type:
            content_type += "; charset=utf-8"
        self._send_bytes(data, 200, content_type)


def run(host: str = "127.0.0.1", port: int = 5000):
    server = ThreadingHTTPServer((host, port), LexerWebHandler)
    print("Team 07 Lexical Analyzer")
    print(f"Open http://{host}:{port} in your browser")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
