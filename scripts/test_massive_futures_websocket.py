from __future__ import annotations

import json
import os
import signal
import sys
from typing import Any

import websocket
from dotenv import load_dotenv


WEBSOCKET_URL = "wss://delayed.massive.com/futures"
DEFAULT_TICKER = "MESU6"
CHANNEL = "AM"


def mask_secret(value: str) -> str:
    """Return a safely masked version of a secret for diagnostic output."""
    if len(value) <= 8:
        return "*" * len(value)

    return f"{value[:4]}...{value[-4:]}"


def parse_messages(raw_message: str) -> list[dict[str, Any]]:
    """Parse Massive's JSON response into a consistent list of messages."""
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

    if not api_key or api_key == "your_massive_api_key_here":
        print(
            "Error: MASSIVE_API_KEY is missing or still contains "
            "the placeholder value."
        )
        return 1

    subscription = f"{CHANNEL}.{ticker}"

    print("Massive Futures WebSocket smoke test")
    print(f"Endpoint:      {WEBSOCKET_URL}")
    print(f"Subscription:  {subscription}")
    print(f"API key:       {mask_secret(api_key)}")
    print("Press Ctrl+C to stop.")
    print()

    authenticated = False
    subscribed = False

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
        nonlocal authenticated, subscribed

        try:
            messages = parse_messages(raw_message)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[ERROR] Unable to parse message: {exc}")
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

            if event_type == CHANNEL:
                print("[DATA] Minute aggregate received:")
                print(json.dumps(message, indent=2, sort_keys=True))
                continue

            print("[MESSAGE]")
            print(json.dumps(message, indent=2, sort_keys=True))

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
        print(f"Close status:  {close_status_code}")
        print(f"Close message: {close_message}")

        if authenticated:
            print("Authentication was confirmed.")
        else:
            print("Authentication was not confirmed.")

        if subscribed:
            print(f"Subscription to {subscription} was confirmed.")
        else:
            print(
                f"Subscription to {subscription} was not explicitly "
                "confirmed."
            )

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

    try:
        ws.run_forever(
            ping_interval=30,
            ping_timeout=10,
        )
    except KeyboardInterrupt:
        ws.close()
    except Exception as exc:
        print(f"[FATAL] Unexpected WebSocket failure: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())