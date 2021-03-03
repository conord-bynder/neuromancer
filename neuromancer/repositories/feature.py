from typing import Type
from uuid import UUID
from sqlalchemy.orm.query import Query

from bynder_connectors.repositories.alchemy import AlchemyBaseRepository

from neuromancer.models.portal_feature import PortalFeature
from neuromancer.models.feature import Feature


class FeatureRepository(AlchemyBaseRepository):  # pragma: no cover
    @property
    def typ(self) -> Type[Feature]:
        return Feature

    def get_portal_features(self, portal_id: UUID) -> Query:
        query = self.list_by()
        query = (
            query.join(PortalFeature)
            .filter(
                PortalFeature.portal_id == portal_id))
        return query
