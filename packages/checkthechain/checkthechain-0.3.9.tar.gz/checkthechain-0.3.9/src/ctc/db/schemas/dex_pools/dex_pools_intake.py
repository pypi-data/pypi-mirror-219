from __future__ import annotations

import typing

import toolsql

from ctc import config
from ctc import spec
from . import dex_pools_statements


async def async_intake_dex_pools(
    *,
    factory: spec.Address,
    dex_pools: typing.Sequence[spec.DexPool],
    last_scanned_block: int | None = None,
    context: spec.Context = None,
) -> None:
    """intake dex pools into database

    - this function should always be provided with the complete set of dex pools
        that have been created since the previous last_scanned_block
    - all dex pools should have the same factory
    """

    # verify factories are identical
    for dex_pool in dex_pools:
        if dex_pool['factory'].lower() != factory:
            raise Exception('all dex pools should be produced by same factory')

    # obtain last scanned block if not provided
    if last_scanned_block is None:
        if len(dex_pools) == 0:
            return
        last_scanned_block = max(
            dex_pool['creation_block'] for dex_pool in dex_pools
        )

    db_config = config.get_context_db_config(
        schema_name='dex_pools',
        context=context,
    )
    async with toolsql.async_connect(db_config) as conn:
        await dex_pools_statements.async_upsert_dex_pools(
            dex_pools=dex_pools,
            conn=conn,
            context=context,
        )
        await dex_pools_statements.async_upsert_dex_pool_factory_query(
            factory=factory,
            last_scanned_block=last_scanned_block,
            conn=conn,
            context=context,
        )
