import pytest

from ctc import evm
from ctc.evm.erc20_utils import erc20_spec


DAI_CONTRACT = "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()
START_BLOCK = 15181140
START_TIMESTAMP = 1658342398
END_BLOCK = 15181147


@pytest.mark.asyncio
async def test_get_events():
    df = await evm.async_get_events(
        contract_address=DAI_CONTRACT,
        event_abi=erc20_spec.erc20_event_abis['Transfer'],
        start_block=START_BLOCK,
        end_block=END_BLOCK,
        include_timestamps=True,
        event_name="Transfer",
    )
    assert len(df) == 6
    assert df["contract_address"][0] == DAI_CONTRACT
    assert df["block_number"][0] == START_BLOCK
    assert df["timestamp"][0] == START_TIMESTAMP
