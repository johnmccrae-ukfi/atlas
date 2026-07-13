from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


from src.common.transformers.massive_futures_minute_aggregate_transformer import (  # noqa: E402
    transform_massive_minute_aggregate,
)


def main() -> int:
    source_message = {
        "c": "7593",
        "dv": "1731135.75",
        "e": 1783930200000,
        "ev": "AM",
        "h": "7593.75",
        "l": "7591.5",
        "n": 108,
        "o": "7592.25",
        "s": 1783930140000,
        "sym": "MESU6",
        "v": 228,
    }

    received_utc = datetime(
        2026,
        7,
        13,
        8,
        20,
        5,
        123000,
        tzinfo=timezone.utc,
    )

    transformed_event = transform_massive_minute_aggregate(
        source_message,
        subscription="AM.MESU6",
        received_utc=received_utc,
    )

    expected_values = {
        "event_type": "AM",
        "symbol": "MESU6",
        "provider_start_epoch_ms": 1783930140000,
        "provider_end_epoch_ms": 1783930200000,
        "event_start_utc": "2026-07-13T08:09:00+00:00",
        "event_end_utc": "2026-07-13T08:10:00+00:00",
        "open_price": "7592.25",
        "high_price": "7593.75",
        "low_price": "7591.5",
        "close_price": "7593",
        "volume": 228,
        "event_count": 108,
        "dollar_volume": "1731135.75",
        "atlas_received_utc": "2026-07-13T08:20:05.123000+00:00",
        "atlas_source": "massive",
        "atlas_feed": "futures_delayed",
        "atlas_subscription": "AM.MESU6",
        "atlas_schema_version": 1,
        "atlas_event_id": "massive|AM|MESU6|1783930140000",
    }

    for field_name, expected_value in expected_values.items():
        actual_value = transformed_event.get(field_name)

        if actual_value != expected_value:
            raise AssertionError(
                f"Field {field_name!r} failed validation: "
                f"expected {expected_value!r}, received {actual_value!r}."
            )

    if transformed_event["raw_payload"] != source_message:
        raise AssertionError(
            "raw_payload does not match the original Massive message."
        )

    if transformed_event["raw_payload"] is source_message:
        raise AssertionError(
            "raw_payload must be a copy rather than the original object."
        )

    json_output = json.dumps(
        transformed_event,
        indent=2,
        sort_keys=True,
    )

    print("Massive futures minute aggregate transformer test")
    print("-------------------------------------------------")
    print(json_output)
    print()
    print("[PASSED] Transformer output matches the expected Atlas envelope.")

    return 0


if __name__ == "__main__":
    sys.exit(main())