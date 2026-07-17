#!/usr/bin/env python3
import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_PORT = 8000
USER_AGENT = "gh-broken-link-recon/1.0"


def request_url(url: str, method: str) -> dict:
    request = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
    )

    try:
        with urllib.request.urlopen(request, context=ssl.create_default_context(), timeout=8) as response:
            if method == "GET":
                response.read(1024)
            return {
                "kind": "http",
                "status": response.status,
            }
    except urllib.error.HTTPError as error:
        return {
            "kind": "http",
            "status": error.code,
        }
    except Exception as error:  # noqa: BLE001
        return {
            "kind": "error",
            "message": str(error) or error.__class__.__name__,
        }


def classify_url(url: str) -> dict:
    head_result = request_url(url, "HEAD")

    if head_result["kind"] == "http" and 200 <= head_result["status"] < 400:
        return {
            "status": "valid",
            "note": f"HEAD {head_result['status']}",
        }

    needs_fallback = (
        head_result["kind"] == "error"
        or (
            head_result["kind"] == "http"
            and head_result["status"] in {401, 403, 405, 429}
        )
    )

    if needs_fallback:
        get_result = request_url(url, "GET")

        if get_result["kind"] == "http" and 200 <= get_result["status"] < 400:
            return {
                "status": "valid",
                "note": f"GET {get_result['status']} after HEAD fallback",
            }

        if get_result["kind"] == "http" and (
            get_result["status"] in {404, 410} or get_result["status"] >= 500
        ):
            return {
                "status": "broken",
                "note": f"GET {get_result['status']}",
            }

        return {
            "status": "review",
            "note": (
                f"GET {get_result['status']}"
                if get_result["kind"] == "http"
                else "Request blocked or inconclusive"
            ),
        }

    if head_result["kind"] == "http" and (
        head_result["status"] in {404, 410} or head_result["status"] >= 500
    ):
        return {
            "status": "broken",
            "note": f"HEAD {head_result['status']}",
        }

    return {
        "status": "review",
        "note": (
            f"HEAD {head_result['status']}"
            if head_result["kind"] == "http"
            else "Request blocked or inconclusive"
        ),
    }


class ScannerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/validate-url":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API endpoint")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON body"})
            return

        url = payload.get("url")
        if not isinstance(url, str) or not url.strip():
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "A non-empty `url` string is required"})
            return

        self._send_json(HTTPStatus.OK, classify_url(url.strip()))

    def _send_json(self, status: HTTPStatus, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve the GitHub broken-link scanner and backend URL validator."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to bind the local server on. Defaults to {DEFAULT_PORT}.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), ScannerHandler)
    print(f"Serving scanner on http://127.0.0.1:{args.port}", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...", flush=True)
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
