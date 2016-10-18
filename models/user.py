from . import url_for
from . import ModelMixin
from . import db

class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(36))
    password = db.Column(db.String(36))
    profile = db.Column(db.String(512), default='')
    admin = db.Column(db.Boolean, default=False)
    bbsContent = db.relationship('bbsContent', backref="author", lazy='dynamic')
    avatar_url = db.Column(db.String(1000))

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar_url = url_for('static', filename='image/tree_small.png')

    def valid_login(self, u):
        if u is not None:
            username_equals = u.username == self.username
            password_equals = u.password == self.password
            status = username_equals and password_equals
            if status:
                return status, '登录成功'
            return status, '登录失败'
        else:
            return False, '登录失败'

    # 验证注册用户的合法性的
    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    #ajax 验证用户是否存在
    def valid_username(self):
        u = User.query.filter_by(username=self.username).first() == None
        if u:
            message = '恭喜你，该用户名可用'
            status = True
        else:
            message = '用户名已被注册,请重新填写'
            status = False
        return status, message

    def is_admin(self):
        return self.admin

    def json(self):
        d = dict(
            username=self.username,
            profile=self.profile,
        )
        return d
