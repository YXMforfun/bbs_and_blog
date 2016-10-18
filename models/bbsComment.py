from . import ModelMixin
from . import db
from . import datetime
from .user import User


class bbsComment(db.Model, ModelMixin):
    __tablename__ = 'bbs_comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('bbs_contents.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.relation(User, innerjoin=True, lazy="joined")


    def __init__(self, form):
        self.comment = form.get('comment', '')

    def get_create_time(self):
        return self.create_time.strftime('%Y-%m-%d %H:%M:%S')
