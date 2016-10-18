from . import ModelMixin
from . import db
from . import datetime
from .user import User


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comment = db.relationship("WeiboComment", backref='weibo', lazy='dynamic')
    author = db.relation(User, innerjoin=True, lazy="joined")

    def __init__(self, form):
        self.body = form.get('body', '')

    def valid(self):
        valid = len(self.body) >= 1
        if valid:
            message = '微博发布成功'
            status = True
        else:
            message = '微博发布失败'
            status = False
        return status, message

    def is_auth(self, u):
        is_auth = u.id == self.author_id
        if is_auth:
            message = '微博已被修改'
            status = True
        else:
            message = '无法操作该微博'
            status = False
        return status, message

    def get_create_time(self):
        return self.create_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_update_time(self):
        return self.update_time.strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        d = dict(
            id=self.id,
            weibo=self.body,
            create_time=self.create_time,
            update_time=self.update_time,
            comment=self.comment.count(),
            author=self.author.username if hasattr(self.author, 'username') else None,
            avatar=self.author.avatar_url if hasattr(self.author, 'avatar_url') else None,
        )
        return d