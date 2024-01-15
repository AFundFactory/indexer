import indexer.models as models
from indexer.types.campaign.storage import CampaignStorage
from indexer.types.campaign.parameter.send_funds import SendFundsParameter
from dipdup.context import HandlerContext
from dipdup.models import Transaction

# import requests, json
from indexer.utils import fetch_profile_tzkt

async def on_fund(
    ctx: HandlerContext,
    fund: Transaction[SendFundsParameter, CampaignStorage],
) -> None:

    funding_address = fund.data.sender_address
    amount = int(fund.data.amount)
    campaign_address = fund.data.target_address

    # profile = requests.get('https://api.tzprofiles.com/' + funding_address).json()

    # username = ''
    # if len(profile) > 0:
    #     for verification in profile:
    #         obj = json.loads(verification[1])
    #         context = obj['@context'][1]
    #         credentialSubject = obj['credentialSubject']
    #         if 'website' in context:
    #             username = credentialSubject['alias']

    profile = fetch_profile_tzkt(funding_address)

    user, _ = await models.UserTable.get_or_create(
        address = funding_address
    )
    user.name = profile['name']
    await user.save()

    await models.FundingTable(
        contract_id = campaign_address, 
        funding_address_id = funding_address,
        date = fund.data.timestamp,
        amount = amount / 1000000,
    ).save()

    campaign = await models.CampaignList.get(contract = campaign_address)
    campaign.donated += amount / 1000000
    await campaign.save()
