from .maintenance_db import db, BaseModel

class Release(BaseModel):
    __tablename__ = 'releases'
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    r_name = db.Column(db.Unicode(20), nullable=False, unique=True)
    description = db.Column(db.Unicode(100), default='')

    @staticmethod
    def insert_fake_release():
        releases = ['DNH0.0', 'DNH2.0', 'DNH3.0', 'DNH4.0', 'DNH5.0',
                    'DNH6.0', 'DNH7.0', 'DNH8.0']
        for c in releases:
            cat = Release.query.filter_by(r_name=c).first()
            if cat is None:
                cat = Release(r_name=c)
                db.session.add(cat)
        db.session.commit()

    def __repr__(self):
        return '<Release %r>' % self.r_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            Release.r_id,
            Release.r_name,
            Release.description
        ]

        res = Release.query.with_entities(*ret_col).filter(db_filter).order_by(order_by).all()
        return res