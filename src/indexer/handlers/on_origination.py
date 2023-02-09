import indexer.models as models
# from indexer.types.ff_main.storage import FfMainStorage
from indexer.types.campaign.storage import CampaignStorage
from dipdup.context import HandlerContext
from dipdup.models import Origination

import requests, json

async def on_origination(
    ctx: HandlerContext,
    campaign_origination: Origination[CampaignStorage],
) -> None:

    contract = campaign_origination.data.originated_contract_address
    owner = campaign_origination.data.storage['owner']
    title = campaign_origination.data.storage['title']
    description = campaign_origination.data.storage['description']
    url = campaign_origination.data.storage['url']
    ascii = campaign_origination.data.storage['ascii']
    category = campaign_origination.data.storage['category']
    goal = campaign_origination.data.storage['goal']
    closed = campaign_origination.data.storage['closed']
    creation_date = campaign_origination.data.timestamp
    version = campaign_origination.data.storage['version']

    # create user
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

    await models.CampaignList(
        contract = contract, 
        owner_id = owner,
        balance = 0,
        donated = 0,
        title = title, 
        description = description,
        url = url,
        ascii = ascii,
        category = category,
        goal = int(goal) / 1000000,
        closed = closed,
        creation_date = creation_date,
        version = version
    ).save()
