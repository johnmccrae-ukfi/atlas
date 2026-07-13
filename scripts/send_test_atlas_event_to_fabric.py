from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from azure.eventhub import EventData, EventHubProducerClient
from dotenv import load_dotenv


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


def main() -> int:
    load_dotenv()

    connection_string = os.getenv(
        "FABRIC_EVENTSTREAM_CONNECTION_STRING"
    )
    event_hub_name = os.getenv(
        "FABRIC_EVENTSTREAM_EVENT_HUB_NAME"
    )

    if not connection_string:
        print(
            "Error: FABRIC_EVENTSTREAM_CONNECTION_STRING is missing."
        )
        return 1

    if not event_hub_name:
        print(
            "Error: FABRIC_EVENTSTREAM_EVENT_HUB_NAME is missing."
        )
        return 1

    atlas_event = {
        "event_type": "AM",
        "symbol": "MESU6",
        "provider_start_epoch_ms": 1783932120000,
        "provider_end_epoch_ms": 1783932180000,
        "event_start_utc": "2026-07-13T08:42:00+00:00",
        "event_end_utc": "2026-07-13T08:43:00+00:00",
        "open_price": "7595.5",
        "high_price": "7595.5",
        "low_price": "7594.75",
        "close_price": "7595.25",
        "volume": 44,
        "event_count": 27,
        "dollar_volume": "334184.25",
        "atlas_received_utc": "2026-07-13T08:53:04.065700+00:00",
        "atlas_source": "massive",
        "atlas_feed": "futures_delayed",
        "atlas_subscription": "AM.MESU6",
        "atlas_schema_version": 1,
        "atlas_event_id": "massive|AM|MESU6|1783932120000",
        "raw_payload": {
            "c": "7595.25",
            "dv": "334184.25",
            "e": 1783932180000,
            "ev": "AM",
            "h": "7595.5",
            "l": "7594.75",
            "n": 27,
            "o": "7595.5",
            "s": 1783932120000,
            "sym": "MESU6",
            "v": 44,
        },
    }

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_string,
        eventhub_name=event_hub_name,
    )

    try:
        event_batch = producer.create_batch()
        event_batch.add(
            EventData(
                json.dumps(
                    atlas_event,
                    separators=(",", ":"),
                )
            )
        )

        producer.send_batch(event_batch)

    except Exception as exc:
        print(f"[FAILED] Unable to send Atlas test event: {exc}")
        return 1

    finally:
        producer.close()

    print("[SENT] One Atlas test event was sent to Fabric Eventstream.")
    print(f"Event ID: {atlas_event['atlas_event_id']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())