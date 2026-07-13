from __future__ import annotations

import json
from typing import Any, Mapping

from azure.eventhub import EventData, EventHubProducerClient


class FabricEventstreamWriter:
    """Send Atlas event envelopes to a Fabric Eventstream custom endpoint."""

    def __init__(
        self,
        connection_string: str,
        event_hub_name: str,
    ) -> None:
        if not connection_string:
            raise ValueError("connection_string must not be empty.")

        if not event_hub_name:
            raise ValueError("event_hub_name must not be empty.")

        self._producer = EventHubProducerClient.from_connection_string(
            conn_str=connection_string,
            eventhub_name=event_hub_name,
        )

    def write_event(
        self,
        event: Mapping[str, Any],
    ) -> None:
        """Serialise and send one Atlas event envelope."""
        event_json = json.dumps(
            dict(event),
            separators=(",", ":"),
        )

        event_batch = self._producer.create_batch()
        event_batch.add(EventData(event_json))
        self._producer.send_batch(event_batch)

    def close(self) -> None:
        """Close the underlying Event Hubs producer."""
        self._producer.close()

    def __enter__(self) -> FabricEventstreamWriter:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()