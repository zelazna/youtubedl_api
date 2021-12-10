from server.crud.crud_base import CRUDBase
from server.models.download import Download


class CrudDownloads(CRUDBase):
    ...


download = CrudDownloads(Download)
