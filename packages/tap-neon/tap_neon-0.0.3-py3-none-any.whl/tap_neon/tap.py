"""Neon Serverless Postgres tap class."""

from __future__ import annotations

import typing as t
from copy import deepcopy

import requests
from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk._singerlib import resolve_schema_references

from tap_neon import streams

if t.TYPE_CHECKING:
    from singer_sdk.streams import RESTStream

OPENAPI_URL = "https://dfv3qgd2ykmrx.cloudfront.net/api_spec/release/v2.json"
STREAMS: list[type[streams.NeonStream]] = [
    streams.Operations,
    streams.Projects,
    streams.Branches,
    streams.Endpoints,
    streams.Roles,
    streams.Databases,
]


def not_required_null(schema: dict[str, t.Any]) -> dict[str, t.Any]:
    """Add 'null' to the type of all properties that are not required."""
    new_schema = deepcopy(schema)
    schema_type: str | list[str] = new_schema.get("type")  # type: ignore[assignment]
    if "object" not in schema_type:
        errmsg = "Schema type must be of 'object' type"
        raise ValueError(errmsg)

    required = new_schema.get("required", [])

    for prop in new_schema.get("properties", {}).values():
        prop_type: str | list[str] = prop.pop("type", [])
        if prop not in required and "null" not in prop_type:
            prop["type"] = (
                [prop_type, "null"]
                if isinstance(prop_type, str)
                else [*prop_type, "null"]
            )

        if "object" in prop_type:
            prop.update(not_required_null(prop))

    return new_schema


class TapNeon(Tap):
    """Singer tap for Neon Serverless Postgres."""

    name = "tap-neon"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="API Key for Neon Serverless Postgres",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def get_openapi_schema(self) -> dict:
        """Retrieve Swagger/OpenAPI schema for this API.

        Returns:
            OpenAPI schema.
        """
        return requests.get(OPENAPI_URL, timeout=5).json()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Neon Serverless Postgres streams.
        """
        streams: list[RESTStream] = []
        openapi_schema = self.get_openapi_schema()

        for stream_type in STREAMS:
            schema = {
                "$ref": f"#/components/schemas/{stream_type.swagger_ref}",
                "components": openapi_schema["components"],
            }
            resolved_schema = not_required_null(resolve_schema_references(schema))
            streams.append(stream_type(tap=self, schema=resolved_schema))

        return sorted(streams, key=lambda x: x.name)
