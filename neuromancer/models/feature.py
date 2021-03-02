from sqlalchemy import Boolean, Column, String

from neuromancer.libs.legacy import CFUUID
from neuromancer.libs.util import ModelUtils
from neuromancer.transactions import ModelBase


class Feature(ModelBase, ModelUtils):
    __tablename__ = "features"

    id = Column(CFUUID(), primary_key=True)
    description = Column(String(255))
    code = Column(String(45))
    is_default = Column('isDefault', Boolean, default=False)
    is_beta = Column(Boolean, default=False)
    is_hidden = Column('isHidden', Boolean, default=False)
