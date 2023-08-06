from __future__ import annotations

import asyncio
import typing

from ctc import evm
from ctc import spec

if typing.TYPE_CHECKING:
    from typing_extensions import Literal

    import tooltime


class DEX:
    """Standardized interface for DEXes

    - All methods should be classmethods or staticmethods
    - The class should never be instantiated
    - Users do not need to use DEX classes directly
        - Functions in dex_utils will call the appropriate DEX methods

    Subclasses should implement the following methods:
    - async_get_new_pools()
    - _async_get_pool_assets_from_node()
    - _async_get_pool_raw_trades()

    Subclasses should specify the following properties:
    - _pool_factories
    """

    _pool_factories: typing.Mapping[
        int, typing.Sequence[spec.Address]
    ] | None = None

    def __init__(self) -> None:
        raise Exception(
            'this class should never be initialized'
            '\n\nuse functions in dex_utils instead'
        )

    #
    # # methods needing subclass implementation
    #

    @classmethod
    async def async_get_new_pools(
        cls,
        *,
        factory: spec.Address,
        start_block: spec.BlockNumberReference | None = None,
        end_block: spec.BlockNumberReference | None = None,
        start_time: tooltime.Timestamp | None = None,
        end_time: tooltime.Timestamp | None = None,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.DexPool]:
        raise NotImplementedError(cls.__name__ + '.async_get_new_pools')

    @classmethod
    async def _async_get_pool_assets_from_node(
        cls,
        pool: spec.Address,
        *,
        block: spec.BlockNumberReference | None = None,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.Address]:
        raise NotImplementedError(cls.__name__ + '.async_get_pool_assets')

    @classmethod
    async def _async_get_pool_raw_trades(
        cls,
        pool: spec.Address,
        *,
        start_block: spec.BlockNumberReference | None = None,
        end_block: spec.BlockNumberReference | None = None,
        start_time: tooltime.Timestamp | None = None,
        end_time: tooltime.Timestamp | None = None,
        include_timestamps: bool = False,
        verbose: bool = False,
        context: spec.Context = None,
    ) -> spec.RawDexTrades:
        raise NotImplementedError(cls.__name__ + '.async_get_pool_trades')

    #
    # # dex metadata
    #

    @classmethod
    def get_dex_name(cls) -> str:
        return cls.__name__.rstrip('DEX')

    @classmethod
    def get_pool_factories(
        cls,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.Address]:
        from ctc import config

        chain_id = config.get_context_chain_id(context)
        if cls._pool_factories is None:
            raise NotImplementedError(cls.__name__ + '._pool_factories')
        if chain_id not in cls._pool_factories:
            raise Exception('unknown network: ' + str(chain_id))
        return cls._pool_factories[chain_id]

    #
    # # multiple pool functions
    #

    @classmethod
    async def async_get_pools(
        cls,
        *,
        factory: spec.Address | None = None,
        all_dex_factories: bool = False,
        assets: typing.Sequence[spec.Address] | None = None,
        start_block: spec.BlockNumberReference | None = None,
        end_block: spec.BlockNumberReference | None = None,
        start_time: tooltime.Timestamp | None = None,
        end_time: tooltime.Timestamp | None = None,
        update: bool = False,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.DexPool]:
        """return pools"""

        factories: typing.Sequence[spec.Address] | None = None
        if all_dex_factories:
            pool_factories = cls.get_pool_factories(context=context)
            if len(pool_factories) == 1:
                factory = pool_factories[0]
                factories = None
            elif len(pool_factories) > 1:
                factory = None
                factories = pool_factories
            else:
                factory = None
                factories = None

        if assets is not None and len(assets) == 0:
            assets = None

        start_block, end_block = await evm.async_resolve_block_range(
            start_block=start_block,
            end_block=end_block,
            start_time=start_time,
            end_time=end_time,
            allow_none=True,
            context=context,
        )

        if start_block is not None:
            start_block = await evm.async_block_number_to_int(
                start_block,
                context=context,
            )
        if end_block is not None:
            end_block = await evm.async_block_number_to_int(
                end_block,
                context=context,
            )

        pools = await cls.async_get_stored_dex_pools(
            factory=factory,
            factories=factories,
            assets=assets,
            start_block=start_block,
            end_block=end_block,
            context=context,
        )

        if update:
            new_pools = await cls.async_update_pools(
                factory=factory,
                factories=factories,
                context=context,
            )

            # filter pools according to function inputs
            new_pools = _filter_pools(
                pools=new_pools,
                assets=assets,
                start_block=start_block,
                end_block=end_block,
            )

            pools = list(pools) + list(new_pools)

        return pools

    @classmethod
    async def async_get_stored_dex_pools(
        cls,
        *,
        factory: spec.Address | None = None,
        factories: typing.Sequence[spec.Address] | None = None,
        assets: typing.Sequence[spec.Address] | None = None,
        start_block: spec.BlockNumberReference | None = None,
        end_block: spec.BlockNumberReference | None = None,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.DexPool]:
        """return pools"""

        from ctc import db

        pools = await db.async_query_dex_pools(
            factory=factory,
            factories=factories,
            assets=assets,
            start_block=start_block,
            end_block=end_block,
            context=context,
        )
        if pools is None:
            pools = []

        return pools

    #
    # # multiple pool updates
    #

    @classmethod
    async def async_update_pools(
        cls,
        *,
        factory: spec.Address | None = None,
        factories: typing.Sequence[spec.Address] | None = None,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.DexPool]:
        """update latest pools of factory"""

        from ctc import db

        # if not factory or factories specified, use all
        if factories is None and factory is None:
            factories = cls.get_pool_factories(context=context)

        # if using multiple factories, call function separately for each
        if factories is not None:
            coroutines = []
            for factory in factories:
                coroutine = cls.async_update_pools(
                    factory=factory,
                    context=context,
                )
                coroutines.append(coroutine)
            results = await asyncio.gather(*coroutines)
            return [dex_pool for result in results for dex_pool in result]

        if factory is None:
            raise Exception('factory should be specified')

        # get new pools
        last_scanned_block = (
            await db.async_query_dex_pool_factory_last_scanned_block(
                factory=factory,
                context=context,
            )
        )
        if last_scanned_block is None:
            from ctc.toolbox import search_utils

            try:
                creation_block = await evm.async_get_contract_creation_block(
                    factory,
                    context=context,
                )
                if creation_block is None:
                    raise Exception(
                        'could not determine factory creation block'
                    )
                last_scanned_block = creation_block - 1
            except search_utils.NoMatchFound:
                last_scanned_block = -1

        latest_block = await evm.async_get_latest_block_number(context=context)

        if last_scanned_block + 1 <= latest_block:
            new_pools = await cls.async_get_new_pools(
                factory=factory,
                start_block=last_scanned_block + 1,
                end_block=latest_block,
                context=context,
            )
            await db.async_intake_dex_pools(
                factory=factory,
                dex_pools=new_pools,
                last_scanned_block=latest_block,
                context=context,
            )

        else:
            new_pools = []

        return new_pools

    #
    # # single pool metadata
    #

    @classmethod
    async def async_get_pool_assets(
        cls,
        pool: spec.Address,
        *,
        block: spec.BlockNumberReference | None = None,
        context: spec.Context = None,
    ) -> typing.Sequence[spec.Address]:
        return await cls._async_get_pool_assets_from_node(
            pool=pool,
            block=block,
            context=context,
        )

    @classmethod
    async def async_get_pool_asset_symbols(
        cls,
        pool: spec.Address,
        *,
        context: spec.Context = None,
    ) -> typing.Sequence[str]:
        assets = await cls.async_get_pool_assets(pool=pool, context=context)
        return await evm.async_get_erc20s_symbols(assets, context=context)

    #
    # # single pool balances
    #

    @classmethod
    async def async_get_pool_balance(
        cls,
        pool: spec.Address,
        asset: spec.Address,
        *,
        factory: spec.Address | None = None,
        normalize: bool = True,
        block: spec.BlockNumberReference | None = None,
        context: spec.Context = None,
    ) -> int | float:
        result = await evm.async_get_erc20_balance(
            wallet=pool,
            token=asset,
            normalize=normalize,
            block=block,
            context=context,
        )
        if result is None:
            raise Exception('invalid result for pool balance')
        return result

    @classmethod
    async def async_get_pool_balances(
        cls,
        pool: spec.Address,
        *,
        factory: spec.Address | None = None,
        normalize: bool = True,
        block: spec.BlockNumberReference | None = None,
        context: spec.Context = None,
    ) -> typing.Mapping[spec.Address, int | float]:
        pool_tokens = await cls.async_get_pool_assets(
            pool=pool, context=context
        )

        if cls.async_get_pool_balance == DEX.async_get_pool_balance:
            balances = await evm.async_get_erc20s_balances(
                wallet=pool,
                tokens=pool_tokens,
                normalize=normalize,
                block=block,
                context=context,
            )
            return dict(zip(pool_tokens, balances))
        else:
            coroutines = []
            for token in pool_tokens:
                coroutine = cls.async_get_pool_balance(
                    pool=pool,
                    asset=token,
                    normalize=normalize,
                    block=block,
                    context=context,
                )
                coroutines.append(coroutine)
            results = await asyncio.gather(*coroutines)
            return dict(zip(pool_tokens, results))

    @classmethod
    async def async_get_pool_balance_by_block(
        cls,
        pool: spec.Address,
        asset: spec.Address,
        *,
        blocks: typing.Sequence[spec.BlockNumberReference],
        factory: spec.Address | None = None,
        normalize: bool = True,
        context: spec.Context = None,
    ) -> typing.Sequence[int | float]:
        return await evm.async_get_erc20_balance_by_block(
            wallet=pool,
            token=asset,
            normalize=normalize,
            blocks=blocks,
            context=context,
        )

    @classmethod
    async def async_get_pool_balances_by_block(
        cls,
        pool: spec.Address,
        *,
        blocks: typing.Sequence[spec.BlockNumberReference],
        factory: spec.Address | None = None,
        normalize: bool = True,
        context: spec.Context = None,
    ) -> typing.Mapping[str, typing.Sequence[int | float]]:
        if len(blocks) == 0:
            raise NotImplementedError('must specify blocks')

        coroutines = [
            cls.async_get_pool_balances(
                pool=pool,
                factory=factory,
                normalize=normalize,
                block=block,
                context=context,
            )
            for block in blocks
        ]
        results = await asyncio.gather(*coroutines)
        balances_by_block: typing.MutableMapping[
            str, typing.MutableSequence[int | float]
        ] = {}
        for result in results:
            for asset, balance in result.items():
                balances_by_block.setdefault(asset, [])
                balances_by_block[asset].append(balance)

        return balances_by_block

    #
    # # single pool swaps functions
    #

    @classmethod
    async def async_get_pool_trades(
        cls,
        pool: spec.Address,
        *,
        start_block: spec.BlockNumberReference | None = None,
        end_block: spec.BlockNumberReference | None = None,
        start_time: tooltime.Timestamp | None = None,
        end_time: tooltime.Timestamp | None = None,
        label: Literal['index', 'symbol', 'address'] = 'index',
        include_timestamps: bool = False,
        normalize: bool = True,
        verbose: bool = False,
        remove_missing_fields: bool = True,
        include_prices: bool = False,
        include_volumes: bool = False,
        context: spec.Context = None,
    ) -> spec.DataFrame:
        import polars as pl

        # queue relevant label data
        if label == 'symbol':
            symbols_coroutine = cls.async_get_pool_asset_symbols(
                pool=pool,
                context=context,
            )
            symbols_task = asyncio.create_task(symbols_coroutine)
        if normalize or label == 'address':
            assets_coroutine = cls.async_get_pool_assets(
                pool=pool,
                context=context,
            )
            assets_task = asyncio.create_task(assets_coroutine)

        output = await cls._async_get_pool_raw_trades(
            pool=pool,
            start_block=start_block,
            end_block=end_block,
            start_time=start_time,
            end_time=end_time,
            include_timestamps=include_timestamps,
            verbose=verbose,
            context=context,
        )

        if remove_missing_fields:
            if 'timestamp' in output and output['timestamp'] is None:
                del output['timestamp']
            if 'recipient' in output and output['recipient'] is None:
                del output['recipient']

        if normalize or label == 'address':
            assets = await assets_task

        # normalize
        if normalize:
            # test for metapools
            if max(output['sold_id']) >= len(assets) or max(
                output['bought_id']
            ) >= len(assets):
                raise NotImplementedError(
                    'normalize not implemented for metapools'
                )

            decimals = await evm.async_get_erc20s_decimals(
                assets,
                context=context,
            )

            sold_decimals = output['sold_id'].apply(lambda i: decimals[i])
            bought_decimals = output['bought_id'].apply(lambda i: decimals[i])
            output['sold_amount'] /= 10**sold_decimals
            output['bought_amount'] /= 10**bought_decimals

        # replace labels
        if label in ['symbol', 'address']:
            if label == 'symbol':
                new_ids = await symbols_task
            elif label == 'address':
                new_ids = assets
            else:
                raise Exception('unknown label format: ' + str(label))

            output['bought_id'] = output['bought_id'].apply(
                lambda i: new_ids[i]
            )
            output['sold_id'] = output['sold_id'].apply(lambda i: new_ids[i])

        df = pl.DataFrame(output)

        if include_prices:
            prices = cls.compute_trade_prices(df, normalized=normalize)
            for key, value in prices.items():
                df = df.with_columns(pl.Series(key, value))
        if include_volumes:
            volumes = cls.compute_trade_volumes(df)
            for key, value in volumes.items():
                df = df.with_columns(pl.Series(key, value))

        return df

    @classmethod
    def compute_trade_volumes(
        cls, df: spec.DataFrame
    ) -> typing.Mapping[str, spec.Series]:
        df['sold_amount']

        all_ids = sorted(
            set(df['sold_id'].unique()) | set(df['bought_id'].unique())
        )

        volumes = {}
        for asset_id in all_ids:
            volumes['volume__' + str(asset_id)] = (
                df['sold_id'] == asset_id
            ) * df['sold_amount'] + (df['bought_id'] == asset_id) * df[
                'bought_amount'
            ]

        return volumes

    @classmethod
    def compute_trade_prices(
        cls,
        df: spec.DataFrame,
        normalized: bool,
    ) -> typing.Mapping[str, spec.Series]:
        import polars as pl

        if not normalized:
            raise Exception('including prices requires normalize=True')

        all_ids = sorted(
            set(df['sold_id'].unique()) | set(df['bought_id'].unique())
        )
        prices: typing.MutableMapping[str, spec.Series] = {}

        # pre-compute quantities
        sold_amount = df['sold_amount'].apply(float)
        bought_amount = df['bought_amount'].apply(float)
        sold_per_bought = sold_amount / bought_amount
        bought_per_sold = bought_amount / sold_amount
        sold_masks = {}
        bought_masks = {}
        for asset_id in all_ids:
            sold_masks[asset_id] = df['sold_id'] == asset_id
            bought_masks[asset_id] = df['bought_id'] == asset_id

        # compute combinations
        for lhs_id in all_ids:
            for rhs_id in all_ids:
                if lhs_id == rhs_id:
                    continue

                key = 'price__' + str(lhs_id) + '__per__' + str(rhs_id)

                sold_lhs_mask = sold_masks[lhs_id]
                sold_rhs_mask = sold_masks[rhs_id]
                bought_lhs_mask = bought_masks[lhs_id]
                bought_rhs_mask = bought_masks[rhs_id]

                values = (
                    sold_lhs_mask.cast(int)
                    * bought_rhs_mask.cast(int)
                    * sold_per_bought
                    + bought_lhs_mask.cast(int)
                    * sold_rhs_mask.cast(int)
                    * bought_per_sold
                )
                df = df.with_columns(
                    pl.Series(key, values)
                )
                if len(all_ids) > 2:
                    combined_mask = (
                        sold_lhs_mask * bought_rhs_mask
                        + bought_lhs_mask * sold_rhs_mask
                    )
                    df[key][~combined_mask] = float('nan')

                prices[key] = values

        return prices

    # should combine adds and removes into single function?
    # @classmethod
    # async def async_get_pool_liquidity_adds(
    #     cls,
    #     pool: spec.Address,
    #     *,
    #     start_block: spec.BlockNumberReference | None = None,
    #     end_block: spec.BlockNumberReference | None = None,
    #     start_time: tooltime.Timestamp | None = None,
    #     end_time: tooltime.Timestamp | None = None,
    #     labels: Literal['index', 'symbol', 'address'] = 'index',
    #     include_timestamps: bool = False,
    #     normalize: bool = True,
    #     network: spec.NetworkReference | None = None,
    #     provider: spec.ProviderReference | None = None,
    #     verbose: bool = False,
    # ) -> spec.DataFrame:
    #     raise NotImplementedError(cls.__name__ + '.async_get_pool_trades')

    # @classmethod
    # async def async_get_pool_liquidity_removes(
    #     cls,
    #     pool: spec.Address,
    #     *,
    #     start_block: spec.BlockNumberReference | None = None,
    #     end_block: spec.BlockNumberReference | None = None,
    #     start_time: tooltime.Timestamp | None = None,
    #     end_time: tooltime.Timestamp | None = None,
    #     labels: Literal['index', 'symbol', 'address'] = 'index',
    #     include_timestamps: bool = False,
    #     normalize: bool = True,
    #     network: spec.NetworkReference | None = None,
    #     provider: spec.ProviderReference | None = None,
    #     verbose: bool = False,
    # ) -> spec.DataFrame:
    #     raise NotImplementedError(cls.__name__ + '.async_get_pool_trades')


def _filter_pools(
    *,
    pools: typing.Sequence[spec.DexPool],
    assets: typing.Sequence[str] | None = None,
    start_block: int | None = None,
    end_block: int | None = None,
) -> typing.Sequence[spec.DexPool]:
    filtered = []

    # filter the new pools according to input arguments
    for pool in pools:
        # check asset filter
        include = True
        if assets is not None:
            keys = ['asset0', 'asset1', 'asset2', 'asset3']
            for asset in assets:
                asset = asset.lower()
                include = any(pool[key] == asset for key in keys)  # type: ignore
                if not include:
                    break
        if not include:
            continue

        # check block range
        if start_block is not None and (
            pool['creation_block'] is None
            or pool['creation_block'] < start_block
        ):
            continue
        if end_block is not None and (
            pool['creation_block'] is None or pool['creation_block'] > end_block
        ):
            continue

        filtered.append(pool)

    return filtered

