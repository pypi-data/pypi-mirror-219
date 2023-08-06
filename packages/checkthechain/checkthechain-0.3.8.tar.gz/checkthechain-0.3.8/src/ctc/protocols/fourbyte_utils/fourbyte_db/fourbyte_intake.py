from __future__ import annotations

import typing

import toolsql

from ctc import config

from .. import fourbyte_spec
from . import fourbyte_statements


#
# # functions
#


async def async_intake_function_signature(
    function_signature: fourbyte_spec.PartialEntry,
) -> None:

    db_config = config.get_context_db_config(schema_name='4byte', context=None)
    async with toolsql.async_connect(db_config) as conn:
        await fourbyte_statements.async_upsert_function_signature(
            function_signature=function_signature,
            conn=conn,
        )


async def async_intake_function_signatures(
    function_signatures: typing.Sequence[fourbyte_spec.PartialEntry],
) -> None:

    if len(function_signatures) == 0:
        return

    db_config = config.get_context_db_config(schema_name='4byte', context=None)
    async with toolsql.async_connect(db_config) as conn:
        await fourbyte_statements.async_upsert_function_signatures(
            function_signatures=function_signatures,
            conn=conn,
        )


#
# # events
#


async def async_intake_event_signature(
    event_signature: fourbyte_spec.PartialEntry,
) -> None:
    db_config = config.get_context_db_config(schema_name='4byte', context=None)
    async with toolsql.async_connect(db_config) as conn:
        await fourbyte_statements.async_upsert_event_signature(
            event_signature=event_signature,
            conn=conn,
        )


async def async_intake_event_signatures(
    event_signatures: typing.Sequence[fourbyte_spec.PartialEntry],
) -> None:
    db_config = config.get_context_db_config(schema_name='4byte', context=None)
    async with toolsql.async_connect(db_config) as conn:
        await fourbyte_statements.async_upsert_event_signatures(
            event_signatures=event_signatures,
            conn=conn,
        )

