from .maintenance_db import db, BaseModel

class Fault(BaseModel):
    __tablename__ = 'faults'
    f_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    f_name = db.Column(db.Unicode(64), nullable=False, unique=True)
    description = db.Column(db.Unicode(100), default='')

    @staticmethod
    def insert_fake_fault():
        pass

    def __repr__(self):
        return '<Fault %r>' % self.f_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            Fault.f_id,
            Fault.f_name,
            Fault.description
        ]

        res = Fault.query.with_entities(*ret_col).filter(db_filter).order_by(order_by).all()
        return res

    @staticmethod
    def update(f_id, fault_dict):
        Fault.query.filter(Fault.f_id==f_id).update(fault_dict)
        db.session.commit()

    @staticmethod
    def insert(fault_dict):
        fault_obj = Fault(**fault_dict)
        db.session.add(fault_obj)
        db.session.commit()

    @staticmethod
    def delete(f_id):
        fault_obj = Fault.query.get(f_id)
        db.session.delete(fault_obj)
        db.session.commit()