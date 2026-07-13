from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping


EXPECTED_EVENT_TYPE = "AM"
EXPECTED_INTERVAL_MILLISECONDS = 60_000
ATLAS_SOURCE = "massive"
ATLAS_FEED = "futures_delayed"
ATLAS_SCHEMA_VERSION = 1

REQUIRED_FIELDS = {
    "ev",
    "sym",
    "s",
    "e",
    "o",
    "h",
    "l",
    "c",
    "v",
    "n",
    "dv",
}


def _require_utc_datetime(value: datetime) -> datetime:
    """Return a timezone-aware datetime normalised to UTC."""
    if value.tzinfo is None:
        raise ValueError("received_utc must be timezone-aware.")

    return value.astimezone(timezone.utc)


def _epoch_milliseconds_to_utc(value: int) -> datetime:
    """Convert Unix epoch milliseconds to a UTC datetime."""
    return datetime.fromtimestamp(
        value / 1_000,
        tz=timezone.utc,
    )


def _validate_decimal_field(
    message: Mapping[str, Any],
    field_name: str,
) -> str:
    """Validate a decimal-compatible provider field and return its text value."""
    value = message[field_name]

    try:
        Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(
            f"Massive field {field_name!r} must contain a valid decimal "
            f"value; received {value!r}."
        ) from exc

    return str(value)


def _validate_integer_field(
    message: Mapping[str, Any],
    field_name: str,
) -> int:
    """Validate an integer provider field and return it as an int."""
    value = message[field_name]

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"Massive field {field_name!r} must contain an integer; "
            f"received {value!r}."
        )

    return value


def transform_massive_minute_aggregate(
    message: Mapping[str, Any],
    *,
    subscription: str,
    received_utc: datetime | None = None,
) -> dict[str, Any]:
    """
    Transform a Massive Futures AM WebSocket event into an Atlas envelope.

    The original provider payload is retained unchanged under ``raw_payload``.
    Price and dollar-volume values remain strings so their exact decimal
    representation survives JSON serialisation.
    """
    missing_fields = REQUIRED_FIELDS.difference(message)

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(
            f"Massive minute aggregate is missing required fields: {missing}."
        )

    event_type = str(message["ev"])
    symbol = str(message["sym"])

    if event_type != EXPECTED_EVENT_TYPE:
        raise ValueError(
            f"Expected Massive event type {EXPECTED_EVENT_TYPE!r}; "
            f"received {event_type!r}."
        )

    if not symbol:
        raise ValueError("Massive field 'sym' must not be empty.")

    expected_subscription = f"{EXPECTED_EVENT_TYPE}.{symbol}"

    if subscription != expected_subscription:
        raise ValueError(
            f"Subscription {subscription!r} does not match payload "
            f"{expected_subscription!r}."
        )

    provider_start_epoch_ms = _validate_integer_field(message, "s")
    provider_end_epoch_ms = _validate_integer_field(message, "e")
    volume = _validate_integer_field(message, "v")
    event_count = _validate_integer_field(message, "n")

    interval_milliseconds = (
        provider_end_epoch_ms - provider_start_epoch_ms
    )

    if interval_milliseconds != EXPECTED_INTERVAL_MILLISECONDS:
        raise ValueError(
            "Massive AM interval must be exactly 60,000 milliseconds; "
            f"received {interval_milliseconds}."
        )

    if volume < 0:
        raise ValueError(
            f"Massive field 'v' must not be negative; received {volume}."
        )

    if event_count < 0:
        raise ValueError(
            f"Massive field 'n' must not be negative; "
            f"received {event_count}."
        )

    open_price = _validate_decimal_field(message, "o")
    high_price = _validate_decimal_field(message, "h")
    low_price = _validate_decimal_field(message, "l")
    close_price = _validate_decimal_field(message, "c")
    dollar_volume = _validate_decimal_field(message, "dv")

    open_decimal = Decimal(open_price)
    high_decimal = Decimal(high_price)
    low_decimal = Decimal(low_price)
    close_decimal = Decimal(close_price)

    if high_decimal < max(open_decimal, low_decimal, close_decimal):
        raise ValueError(
            "Massive minute aggregate failed OHLC validation: "
            "high is below another price."
        )

    if low_decimal > min(open_decimal, high_decimal, close_decimal):
        raise ValueError(
            "Massive minute aggregate failed OHLC validation: "
            "low is above another price."
        )

    received_timestamp = _require_utc_datetime(
        received_utc or datetime.now(timezone.utc)
    )

    event_start_utc = _epoch_milliseconds_to_utc(
        provider_start_epoch_ms
    )
    event_end_utc = _epoch_milliseconds_to_utc(
        provider_end_epoch_ms
    )

    atlas_event_id = (
        f"{ATLAS_SOURCE}|{event_type}|{symbol}|"
        f"{provider_start_epoch_ms}"
    )

    return {
        "event_type": event_type,
        "symbol": symbol,
        "provider_start_epoch_ms": provider_start_epoch_ms,
        "provider_end_epoch_ms": provider_end_epoch_ms,
        "event_start_utc": event_start_utc.isoformat(),
        "event_end_utc": event_end_utc.isoformat(),
        "open_price": open_price,
        "high_price": high_price,
        "low_price": low_price,
        "close_price": close_price,
        "volume": volume,
        "event_count": event_count,
        "dollar_volume": dollar_volume,
        "atlas_received_utc": received_timestamp.isoformat(),
        "atlas_source": ATLAS_SOURCE,
        "atlas_feed": ATLAS_FEED,
        "atlas_subscription": subscription,
        "atlas_schema_version": ATLAS_SCHEMA_VERSION,
        "atlas_event_id": atlas_event_id,
        "raw_payload": deepcopy(dict(message)),
    }