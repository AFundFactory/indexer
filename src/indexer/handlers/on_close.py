import indexer.models as models
from indexer.types.campaign.storage import CampaignStorage
from indexer.types.campaign.parameter.close_campaign import CloseCampaignParameter
from dipdup.context import HandlerContext
from dipdup.models import Transaction

import requests, json

async def on_close(
    ctx: HandlerContext,
    close: Transaction[CloseCampaignParameter, CampaignStorage],
) -> None:
    
    campaign_address = close.data.target_address

    campaign = await models.CampaignList.get(contract = campaign_address)
    campaign.closed = True
    await campaign.save()

    # update username
    owner = close.data.sender_address
    profile = requests.get('https://api.tzprofiles.com/' + owner).json()

    username = ''
    if len(profile) > 0:
        for verification in profile:
            obj = json.loads(verification[1])
            context = obj['@context'][1]
            credentialSubject = obj['credentialSubject']
            if 'website' in context:
                username = credentialSubject['alias']

    user, _ = await models.UserTable.get_or_create(
        address = owner
    )
    user.name = username
    await user.save()