import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

spec = importlib.util.spec_from_file_location("tv3_event_server", Path(__file__).resolve().parents[1] / "tools/tv3_event_server.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EventServerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), module.make_handler(str(Path(self.temp.name) / "events.sqlite3"), "test-only-token"))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/api/v1/warehouse/events"
        self.event = {"eventId": "event-1", "eventType": "EVENT_DISPATCH_COMPLETED", "aggregateId": "PX-1", "createdAt": "2026-11-16T15:00:00Z", "payload": {"serials": ["RLX-1"]}}

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def send(self, event=None, token="test-only-token", key=None):
        event = event or self.event
        request = Request(self.url, data=json.dumps(event).encode(), method="POST", headers={"Content-Type": "application/json", "Authorization": "Bearer " + token, "Idempotency-Key": key or event["eventId"]})
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            with error:
                return error.code, json.load(error)

    def test_unauthenticated_event_is_not_stored(self):
        self.assertEqual(401, self.send(token="wrong")[0])
        self.assertEqual(200, self.send()[0])

    def test_retry_is_acknowledged_once(self):
        first, second = self.send()[1], self.send()[1]
        self.assertEqual(first["sequence"], second["sequence"])
        self.assertTrue(second["duplicate"])

    def test_id_cannot_be_reused_for_different_payload(self):
        self.send()
        changed = {**self.event, "payload": {"serials": ["DIFFERENT"]}}
        self.assertEqual(409, self.send(changed)[0])

    def test_idempotency_key_is_required(self):
        self.assertEqual(400, self.send(key="wrong-id")[0])

    def test_concurrent_retries_create_one_record_and_cursor(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.send(), range(12)))
        self.assertTrue(all(status == 200 for status, _ in results))
        self.assertEqual(1, len({body["sequence"] for _, body in results}))
        request = Request(self.url + "?after=0", headers={"Authorization": "Bearer test-only-token"})
        with urlopen(request) as response:
            data = json.load(response)
        self.assertEqual(1, len(data["events"]))
        self.assertEqual(1, data["nextCursor"])


if __name__ == "__main__":
    unittest.main()
