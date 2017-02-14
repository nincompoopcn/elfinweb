from .maintenance_db import db, BaseModel

class Privilege(BaseModel):
    __tablename__ = 'privileges'
    u_id = db.Column(db.Unicode(20), nullable=False, primary_key=True)
    level = db.Column(db.Integer, nullable=False)

    @staticmethod
    def insert_fake_privilege():
        users = ['zhongtli']
        for u in users:
            user = Privilege.query.filter_by(u_id=u).first()
            if user is None:
                user = Privilege(u_id=u, level=9)
                db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<Privilege %r>' % self.u_id

    @staticmethod
    def select(db_filter=True):
        ret_col =  [
            Privilege.u_id,
            Privilege.level,
        ]

        res = Privilege.query.with_entities(*ret_col).filter(db_filter).order_by(Privilege.level.desc(), Privilege.u_id).all()
        return res

    @staticmethod
    def insert(privilege_dict):
        privilege_obj = Privilege(**privilege_dict)
        db.session.add(privilege_obj)
        db.session.commit()

    @staticmethod
    def delete(u_id):
        privilege_obj = Privilege.query.get(u_id)
        db.session.delete(privilege_obj)
        db.session.commit()