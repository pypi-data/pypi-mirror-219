import glob
import os
import json
from typing import Any, List, Optional

import click
from gable.client import GableClient
from gable.readers.dbapi import DbapiReader
from gable.readers.file import get_file


def post_contract_check_request(
    client: GableClient,
    contract_id: str,
    source_type: str,
    schema_contents: str,
) -> tuple[str, bool]:
    result, success, status_code = client.post(
        f"v0/contract/{contract_id}/check",
        json={
            "sourceType": source_type,
            "schemaContents": schema_contents,
        },
    )
    return str(result["message"]), success


def post_data_asset_check_requests(
    client: GableClient,
    source_type: str,
    source_names: List[str],
    realDbName: str,
    realDbSchema: str,
    schema_contents: List[str],
) -> list[tuple[str, str, int]]:
    # If this is a database, there might be multiple table's schemas within the information schema
    # returned from the DbApi reader. In that case, we need to post each table's schema separately.
    if source_type in ["postgres", "mysql"]:
        # For DBs we get back the entire information schema in a single string
        schema_contents_str = schema_contents[0]
        source_name = source_names[0]
        information_schema = json.loads(schema_contents_str)
        grouped_table_schemas: dict[str, List[Any]] = {}
        for information_schema_row in information_schema:
            if information_schema_row["TABLE_NAME"] not in grouped_table_schemas:
                grouped_table_schemas[information_schema_row["TABLE_NAME"]] = []
            grouped_table_schemas[information_schema_row["TABLE_NAME"]].append(
                information_schema_row
            )
        # Post each table's schema separately
        results = []
        for table_name, table_schema in grouped_table_schemas.items():
            result, success, status_code = client.post(
                "v0/data-asset/check",
                json={
                    "sourceType": source_type,
                    "sourceName": source_name,
                    "realDbName": realDbName,
                    "realDbSchema": realDbSchema,
                    "schemaContents": json.dumps(table_schema),
                },
            )
            results.append(
                (
                    f"{realDbName}.{realDbSchema}.{table_name}",
                    result["message"],
                    status_code,
                )
            )
        return results
    # For non-database sources, just post the schemas
    results = []
    for source_name, schema in zip(source_names, schema_contents):
        result, success, status_code = client.post(
            "v0/data-asset/check",
            json={
                "sourceType": source_type,
                "sourceName": source_name,
                "schemaContents": schema,
            },
        )
        results.append(
            (
                source_name,
                result["message"],
                status_code,
            )
        )
    return results
