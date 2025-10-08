import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from rp_handler_cpu import handler


class Handler(BaseHTTPRequestHandler):
	def _set_headers(self, status: int = 200):
		self.send_response(status)
		self.send_header("Content-Type", "application/json")
		self.end_headers()

	def do_POST(self):  # noqa: N802 (HTTP method name)
		if self.path not in ("/run", "/rpc"):
			self._set_headers(404)
			self.wfile.write(json.dumps({"error": "not_found"}).encode())
			return

		length = int(self.headers.get("Content-Length", "0"))
		body = self.rfile.read(length) if length else b"{}"
		try:
			payload = json.loads(body.decode("utf-8"))
		except Exception:
			self._set_headers(400)
			self.wfile.write(json.dumps({"error": "invalid_json"}).encode())
			return

		try:
			result = handler(payload)
			self._set_headers(200)
			self.wfile.write(json.dumps(result).encode())
		except Exception as e:
			self._set_headers(500)
			self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())


def run():
	port = int(os.environ.get("PORT", "8080"))
	server = HTTPServer(("0.0.0.0", port), Handler)
	print(f"[local_api] Listening on 0.0.0.0:{port} (POST /run)")
	server.serve_forever()


if __name__ == "__main__":
	run()
