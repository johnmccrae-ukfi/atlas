from __future__ import annotations

import json
import os
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import websocket
from dotenv import load_dotenv


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


from src.common.transformers.massive_futures_minute_aggregate_transformer import (  # noqa: E402
    transform_massive_minute_aggregate,
)
from src.common.writers.FabricEventstreamWriter import (  # noqa: E402
    FabricEventstreamWriter,
)


WEBSOCKET_URL = "wss://delayed.massive.com/futures"
DEFAULT_TICKER = "MESU6"
CHANNEL = "AM"

MASSIVE_API_KEY_PLACEHOLDER = "your_massive_api_key_here"
FABRIC_CONNECTION_STRING_PLACEHOLDER = (
    "your_fabric_eventstream_connection_string_here"
)
FABRIC_EVENT_HUB_NAME_PLACEHOLDER = "your_fabric_event_hub_name_here"


def parse_messages(raw_message: str) -> list[dict[str, Any]]:
    """Parse a Massive WebSocket response into a consistent message list."""
    payload = json.loads(raw_message)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        return [payload]

    raise ValueError(
        f"Unexpected WebSocket payload type: {type(payload).__name__}"
    )


def main() -> int:
    load_dotenv()

    api_key = os.getenv("MASSIVE_API_KEY")
    ticker = os.getenv("MASSIVE_FUTURES_TICKER", DEFAULT_TICKER)

    fabric_connection_string = os.getenv(
        "FABRIC_EVENTSTREAM_CONNECTION_STRING"
    )
    fabric_event_hub_name = os.getenv(
        "FABRIC_EVENTSTREAM_EVENT_HUB_NAME"
    )

    if not api_key or api_key == MASSIVE_API_KEY_PLACEHOLDER:
        print(
            "Error: MASSIVE_API_KEY is missing or still contains "
            "the placeholder value."
        )
        return 1

    if not ticker:
        print("Error: MASSIVE_FUTURES_TICKER must not be empty.")
        return 1

    if (
        not fabric_connection_string
        or fabric_connection_string
        == FABRIC_CONNECTION_STRING_PLACEHOLDER
    ):
        print(
            "Error: FABRIC_EVENTSTREAM_CONNECTION_STRING is missing "
            "or still contains the placeholder value."
        )
        return 1

    if (
        not fabric_event_hub_name
        or fabric_event_hub_name
        == FABRIC_EVENT_HUB_NAME_PLACEHOLDER
    ):
        print(
            "Error: FABRIC_EVENTSTREAM_EVENT_HUB_NAME is missing "
            "or still contains the placeholder value."
        )
        return 1

    subscription = f"{CHANNEL}.{ticker}"

    print("Atlas Massive Futures streaming adapter")
    print(f"Massive endpoint:    {WEBSOCKET_URL}")
    print(f"Subscription:        {subscription}")
    print("Fabric destination:  Eventstream custom endpoint")
    print("Output:              Local log and Fabric Eventstream")
    print("Press Ctrl+C to stop.")
    print()

    authenticated = False
    subscribed = False
    sent_event_count = 0

    try:
        eventstream_writer = FabricEventstreamWriter(
            connection_string=fabric_connection_string,
            event_hub_name=fabric_event_hub_name,
        )
    except Exception as exc:
        print(
            "[FATAL] Unable to create the Fabric Eventstream writer: "
            f"{exc}"
        )
        return 1

    def on_open(ws: websocket.WebSocketApp) -> None:
        print("[CONNECTED] WebSocket connection established.")

        auth_message = {
            "action": "auth",
            "params": api_key,
        }

        ws.send(json.dumps(auth_message))
        print("[AUTH] Authentication request sent.")

    def on_message(
        ws: websocket.WebSocketApp,
        raw_message: str,
    ) -> None:
        nonlocal authenticated
        nonlocal subscribed
        nonlocal sent_event_count

        received_utc = datetime.now(timezone.utc)

        try:
            messages = parse_messages(raw_message)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[ERROR] Unable to parse WebSocket message: {exc}")
            print(f"[RAW] {raw_message}")
            return

        for message in messages:
            event_type = message.get("ev")

            if event_type == "status":
                status = message.get("status")
                status_message = message.get("message")

                print(
                    f"[STATUS] status={status!r}, "
                    f"message={status_message!r}"
                )

                if status == "auth_success" and not authenticated:
                    authenticated = True
                    print("[AUTHENTICATED] Massive accepted the API key.")

                    subscribe_message = {
                        "action": "subscribe",
                        "params": subscription,
                    }

                    ws.send(json.dumps(subscribe_message))
                    print(
                        f"[SUBSCRIBE] Subscription request sent for "
                        f"{subscription}."
                    )

                elif status == "success":
                    message_text = str(status_message or "").lower()

                    if "subscribed" in message_text:
                        subscribed = True
                        print(
                            f"[SUBSCRIBED] Massive accepted "
                            f"{subscription}."
                        )

                elif status in {
                    "auth_failed",
                    "error",
                    "not_authorized",
                }:
                    print("[FAILED] Massive rejected the request.")
                    ws.close()

                continue

            if event_type != CHANNEL:
                print("[IGNORED] Non-minute-aggregate message received:")
                print(json.dumps(message, indent=2, sort_keys=True))
                continue

            try:
                atlas_event = transform_massive_minute_aggregate(
                    message,
                    subscription=subscription,
                    received_utc=received_utc,
                )
            except (KeyError, TypeError, ValueError) as exc:
                print(
                    "[TRANSFORM-ERROR] Unable to create Atlas envelope: "
                    f"{exc}"
                )
                print("[RAW]")
                print(json.dumps(message, indent=2, sort_keys=True))
                continue

            try:
                eventstream_writer.write_event(atlas_event)
            except Exception as exc:
                print(
                    "[FABRIC-ERROR] Unable to send Atlas event to "
                    f"Fabric: {exc}"
                )
                print(
                    "[UNSENT-EVENT] "
                    f"{atlas_event.get('atlas_event_id', '<unknown>')}"
                )
                continue

            sent_event_count += 1

            print(
                f"[ATLAS-EVENT] Transformed and sent minute aggregate "
                f"#{sent_event_count}:"
            )
            print(
                json.dumps(
                    atlas_event,
                    indent=2,
                    sort_keys=True,
                )
            )

    def on_error(
        ws: websocket.WebSocketApp,
        error: object,
    ) -> None:
        print(f"[ERROR] WebSocket error: {error}")

    def on_close(
        ws: websocket.WebSocketApp,
        close_status_code: int | None,
        close_message: str | None,
    ) -> None:
        print()
        print("[CLOSED] WebSocket connection closed.")
        print(f"Close status:             {close_status_code}")
        print(f"Close message:            {close_message}")
        print(f"Authentication confirmed: {authenticated}")
        print(f"Subscription confirmed:   {subscribed}")
        print(f"Atlas events sent:         {sent_event_count}")

    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    def handle_shutdown(
        signum: int,
        frame: object,
    ) -> None:
        print("\n[STOPPING] Closing WebSocket connection...")
        ws.close()

    signal.signal(signal.SIGINT, handle_shutdown)

    exit_code = 0

    try:
        ws.run_forever(
            ping_interval=30,
            ping_timeout=10,
        )
    except KeyboardInterrupt:
        ws.close()
    except Exception as exc:
        print(f"[FATAL] Unexpected streaming-adapter failure: {exc}")
        exit_code = 1
    finally:
        try:
            eventstream_writer.close()
            print("[FABRIC] Eventstream writer closed.")
        except Exception as exc:
            print(
                "[WARNING] Fabric Eventstream writer did not close "
                f"cleanly: {exc}"
            )

            if exit_code == 0:
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())