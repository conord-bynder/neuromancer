from typing import Type

from bynder_connectors.repositories.alchemy import AlchemyBaseRepository
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from neuromancer.models.portal import Portal


class PortalRepository(AlchemyBaseRepository):
    @property
    def typ(self) -> Type[Portal]:
        return Portal
