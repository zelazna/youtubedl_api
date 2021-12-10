from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text

from server.crud.crud_base import CRUDBase
from server.models.request import Request, State
from server.schemas.requests import RequestCreate


class CrudRequests(CRUDBase):
    def set_state(self, db: Session, request: Request, state: State):
        return self.update(db, db_obj=request, obj_in={"state": state})

    def create_with_owner(
        self, db: Session, *, obj_in: RequestCreate, owner_id: int
    ) -> Request:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "id desc",
    ) -> list[Request]:
        return (
            db.query(self.model)
            .order_by(text(order_by))
            .filter(Request.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


request = CrudRequests(Request)
