from sqlalchemy.orm.session import Session

from server.core import CRUDBase, Request, State


class CrudDownloads(CRUDBase):
    def set_in_progress(self, db: Session, request: Request):
        return self.update(db, db_obj=request, obj_in={"state": State.in_progress})

    def set_done(self, db: Session, request: Request):
        return self.update(db, db_obj=request, obj_in={"state": State.done})

    def set_in_error(self, db: Session, request: Request):
        return self.update(db, db_obj=request, obj_in={"state": State.in_error})


requests = CrudDownloads(Request)
