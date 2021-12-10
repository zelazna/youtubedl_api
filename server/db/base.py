# Import all the models, so that Base has them before being
# imported by Alembic
from server.db.base_class import Base  # noqa
from server.models.download import Download  # noqa
from server.models.request import Request  # noqa
from server.models.user import User  # noqa
