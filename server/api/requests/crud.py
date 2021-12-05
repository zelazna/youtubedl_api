from server.core import CRUDBase, Request, State
from sqlalchemy.orm.session import Session


class CrudRequests(CRUDBase):
    def set_state(self, db: Session, request: Request, state: State):
        return self.update(db, db_obj=request, obj_in={"state": state})


requests = CrudRequests(Request)
