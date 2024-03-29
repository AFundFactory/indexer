# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class CampaignStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    ascii: str
    category: str
    closed: bool
    description: str
    url: str
    goal: str
    owner: str
    title: str
    version: str
