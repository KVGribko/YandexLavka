from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all_obj(self, db: Session, limit: int = 1, offset: int = 0):
        return [
            obj.to_dict()
            for obj in db.query(self.model)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        ]

    def get_obj_by_id(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).one_or_none()

    def create_obj(self, db: Session, model, **kwargs):
        obj = model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_or_create(self, db: Session, model, **kwargs):
        obj = db.query(model).filter_by(**kwargs).one_or_none()
        return self.create_obj(db, model, **kwargs) if obj is None else obj

    @staticmethod
    def _get_working_hours(working_hours, hours_model):
        wh = []
        for hour in working_hours:
            from_time, to_time = hour.split("-")
            wh.append(hours_model(from_time=from_time, to_time=to_time))
        return wh
