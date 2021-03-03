from typing import Type

from bynder_connectors.repositories.alchemy import AlchemyBaseRepository

from neuromancer.models.portal_feature import PortalFeature


class PortalFeatureRepository(AlchemyBaseRepository):  # pragma: no cover
    """ PortalFeature repository for all main database interactions.
    """
    @property
    def typ(self) -> Type[PortalFeature]:
        return PortalFeature
