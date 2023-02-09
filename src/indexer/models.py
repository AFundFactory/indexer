from tortoise.fields.relational import ForeignKeyFieldInstance
from tortoise import fields
from dipdup.models import Model
from tortoise.timezone import now

class UserTable(Model):
    address = fields.CharField(36, pk=True)
    name = fields.CharField(50, default='')

class CampaignList(Model):
    contract = fields.CharField(36, pk=True)
    owner: ForeignKeyFieldInstance[UserTable] = fields.ForeignKeyField('models.UserTable', False)
    donated = fields.FloatField()
    title = fields.CharField(50)
    description = fields.CharField(1000)
    url = fields.CharField(1000)
    ascii = fields.CharField(1000)
    category = fields.CharField(30)
    goal = fields.FloatField()
    closed = fields.BooleanField()
    creation_date = fields.DatetimeField()
    version = fields.CharField(5)

class FundingTable(Model):
    id = fields.IntField(pk=True)
    contract: ForeignKeyFieldInstance[CampaignList] = fields.ForeignKeyField('models.CampaignList', 'funding')
    funding_address: ForeignKeyFieldInstance[UserTable] = fields.ForeignKeyField('models.UserTable', False)
    amount = fields.FloatField(default=0)
    date = fields.DatetimeField(default = now())
   
