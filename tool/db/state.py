from .maintenance_db import db, BaseModel

class State(BaseModel):
    __tablename__ = 'states'
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.Unicode(20), nullable=False, unique=True)
    description = db.Column(db.Unicode(100), default='')

    @staticmethod
    def insert_fake_states():
        states = ['Ongoing', 'New', 'Blocked', 'Transfered', 'Closed']
        for c in states:
            cat = State.query.filter_by(s_name=c).first()
            if cat is None:
                cat = State(s_name=c)
                db.session.add(cat)
        db.session.commit()

    def __repr__(self):
        return '<State %r>' % self.s_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            State.s_id,
            State.s_name,
            State.description
        ]

        res = State.query.with_entities(*ret_col).filter(db_filter).order_by(order_by).all()
        return res