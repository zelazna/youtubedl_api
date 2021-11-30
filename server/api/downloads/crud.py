from server.core import CRUDBase

from .models import Download


class CrudDownloads(CRUDBase):
    ...


downloads = CrudDownloads(Download)
