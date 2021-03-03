from sqlalchemy import Column, ForeignKey

from neuromancer.libs.legacy import CFUUID
from neuromancer.libs.util import ModelUtils
from neuromancer.transactions import ModelBase


class PortalFeature(ModelBase, ModelUtils):
    __tablename__ = "account_features"

    feature_id = Column(
        'featureid', CFUUID(), ForeignKey('features.id'), primary_key=True)
    portal_id = Column(
        'accountid', CFUUID(), ForeignKey('accounts.id'), primary_key=True)
