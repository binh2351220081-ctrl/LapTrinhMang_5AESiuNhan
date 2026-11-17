"""Small authenticated, idempotent LAN event journal for the TV3 warehouse demo.

This is an event journal, not a central inventory allocator. It deliberately does not
claim to resolve stock conflicts between independent offline Room databases.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import sqlite3
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


@contextmanager
def open_database(path: str):
    conn = sqlite3.connect(path, timeout=15)
    try:
        yield conn
    finally:
        conn.close()


def make_handler(database_path: str, token: str):
    with open_database(database_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""CREATE TABLE IF NOT EXISTS events (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL UNIQUE,
            content_hash TEXT NOT NULL,
            envelope TEXT NOT NULL,
            received_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
        )""")
        conn.commit()

    class Handler(BaseHTTPRequestHandler):
        server_version = "ChronoVaultEventJournal/1"

        def log_message(self, format, *args):
            # Never log credentials or event payloads.
            return

        def reply(self, code: int, value: dict):
            body = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def authorized(self) -> bool:
            incoming = self.headers.get("Authorization", "")
            if not hmac.compare_digest(incoming.encode(), ("Bearer " + token).encode()):
                self.reply(401, {"success": False, "message": "Authentication required"})
                return False
            return True

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == "/health":
                self.reply(200, {"success": True, "service": "warehouse-event-journal"})
                return
            if parsed.path != "/api/v1/warehouse/events":
                self.reply(404, {"success": False, "message": "Not found"})
                return
            if not self.authorized():
                return
            try:
                query = parse_qs(parsed.query)
                after = max(0, int(query.get("after", ["0"])[0]))
                limit = min(100, max(1, int(query.get("limit", ["100"])[0])))
            except ValueError:
                self.reply(400, {"success": False, "message": "Invalid cursor"})
                return
            with open_database(database_path) as conn:
                rows = conn.execute("SELECT sequence, envelope, received_at FROM events WHERE sequence > ? ORDER BY sequence LIMIT ?", (after, limit)).fetchall()
            events = [{"sequence": row[0], "event": json.loads(row[1]), "receivedAt": row[2]} for row in rows]
            self.reply(200, {"success": True, "events": events, "nextCursor": rows[-1][0] if rows else after})

        def do_POST(self):
            if urlparse(self.path).path != "/api/v1/warehouse/events":
                self.reply(404, {"success": False, "message": "Not found"})
                return
            if not self.authorized():
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 1_048_576:
                    raise ValueError("Invalid content length")
                def no_constant(value):
                    raise ValueError("Non-finite JSON number")
                event = json.loads(self.rfile.read(length), parse_constant=no_constant)
                if not isinstance(event, dict):
                    raise ValueError("JSON object required")
                for field in ("eventId", "eventType", "aggregateId", "createdAt"):
                    if not isinstance(event.get(field), str) or not event[field].strip() or len(event[field]) > 200:
                        raise ValueError("Missing or invalid " + field)
                if not isinstance(event.get("payload"), (dict, list)):
                    raise ValueError("Object or array payload required")
                if self.headers.get("Idempotency-Key") != event["eventId"]:
                    raise ValueError("Idempotency-Key must match eventId")
                envelope = json.dumps(event, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
                digest = hashlib.sha256(envelope.encode()).hexdigest()
            except (ValueError, TypeError, UnicodeError) as error:
                self.reply(400, {"success": False, "message": str(error)})
                return
            with open_database(database_path) as conn:
                conn.execute("BEGIN IMMEDIATE")
                previous = conn.execute("SELECT sequence, content_hash FROM events WHERE event_id = ?", (event["eventId"],)).fetchone()
                if previous:
                    if previous[1] != digest:
                        self.reply(409, {"success": False, "message": "Event ID already used for different data"})
                        return
                    sequence, duplicate = previous[0], True
                else:
                    cursor = conn.execute("INSERT INTO events(event_id, content_hash, envelope) VALUES (?, ?, ?)", (event["eventId"], digest, envelope))
                    sequence, duplicate = cursor.lastrowid, False
                conn.commit()
            self.reply(200, {"success": True, "eventId": event["eventId"], "sequence": sequence, "duplicate": duplicate})

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--database", default="tv3-events.sqlite3")
    args = parser.parse_args()
    token = os.environ.get("CHRONOVAULT_SYNC_TOKEN", "").strip()
    if not token:
        parser.error("Set CHRONOVAULT_SYNC_TOKEN to a nonempty private token before starting.")
    Path(args.database).resolve().parent.mkdir(parents=True, exist_ok=True)
    with open_database(args.database):
        pass
    server = ThreadingHTTPServer((args.host, args.port), make_handler(args.database, token))
    print(f"Warehouse event journal listening on {args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
