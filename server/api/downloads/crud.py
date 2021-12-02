from server.core import CRUDBase, Download


class CrudDownloads(CRUDBase):
    ...


downloads = CrudDownloads(Download)
