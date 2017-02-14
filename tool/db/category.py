from .maintenance_db import db, BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    c_name = db.Column(db.Unicode(64), nullable=False, unique=True)
    description = db.Column(db.Unicode(100), default='')

    @staticmethod
    def insert_fake_category():
        categories = ['EDA', 'LogImprovement', 'Monsho', 'Pronto',
                      'PreCheck', 'RCA', 'Support', 'Yokoten']
        for c in categories:
            cat = Category.query.filter_by(c_name=c).first()
            if cat is None:
                cat = Category(c_name=c)
                db.session.add(cat)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.c_name

    @staticmethod
    def select(db_filter=True, order_by=None):
        ret_col =  [
            Category.c_id,
            Category.c_name,
            Category.description
        ]

        res = Category.query.with_entities(*ret_col).filter(db_filter).order_by(order_by).all()
        return res