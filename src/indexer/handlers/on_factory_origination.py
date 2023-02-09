from typing import cast
from dipdup.context import HandlerContext
from dipdup.models import Origination
from indexer.types.ff_main.storage import FfMainStorage
# import indexer.models as models

async def on_factory_origination(
    ctx: HandlerContext,
    ff_origination: Origination[FfMainStorage],
) -> None:
    
    address = ff_origination.originated_contract_address
    originated_contract = cast(str, address)
    name = f'campaign_template_{originated_contract}'
    await ctx.add_contract(
        name=originated_contract,
        address=originated_contract,
        typename='campaign',
    )

    await ctx.add_index(
        name=name,
        template='campaign_template',
        values={'contract': originated_contract},
    )

    