# simulator.py
from __future__ import annotations

import logging
import os
import sys
import time

from utils import *

# ==============================
# ENV Var
# ==============================
DEVICES_FILE: str = os.getenv("DEVICES_FILE", "devices.json")
INTERVAL: float = get_env_float("INTERVAL", 10.0)     # default 10s

REMOTE: str = os.getenv("REMOTE", "localhost:8080")
REMOTE = REMOTE.rstrip("/")


if not REMOTE:
    print("ERROR: REMOTE environment variable is required.", file=sys.stderr)
    sys.exit(1)

# ==============================
# Logging
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# ==============================
# Main loop
# ==============================
def main() -> None:
    logging.info("Starting telemetry simulator")
    logging.info("REMOTE=%s", REMOTE)
    logging.info("INTERVAL=%.2f seconds", INTERVAL)
    logging.info("DEVICES_FILE=%s", DEVICES_FILE)

    try:
        # load json
        devices = load_devices(DEVICES_FILE)
    except Exception as exc:
        logging.error("Failed to load devices: %s", exc)
        sys.exit(1)

    try:
        while True:
            start = time.time()
            logging.info("Sending telemetry for %d devices", len(devices))

            # loop all devices
            for device in devices:
                (x_cood, y_cood) = random_coordinates()
                payload = build_payload(now_utc_iso())
                target_url = f"http://{REMOTE}/api/telemetry"
                send_telemetry(device, target_url, payload)

            # set interval
            elapsed = time.time() - start
            sleep_for = max(0.0, INTERVAL - elapsed)

            logging.info(
                "Cycle complete in %.2fs, sleeping for %.2fs", elapsed, sleep_for)
            time.sleep(sleep_for)
    except KeyboardInterrupt:
        logging.info("Received Ctrl+C, shutting down.")


if __name__ == "__main__":
    main()
