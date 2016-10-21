from flask import session, request, url_for, redirect, abort
from models.user import User
import json
from datetime import datetime, date
from functools import wraps
from urllib.parse import urlparse, urljoin

def log(*args):
    print(*args)


def current_user():
    uid = session.get('uid')
    if uid is not None:
        u = User.query.get(uid)
        return u

def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u_id = session.get('uid')
        if not User.query.get(u_id).is_admin() :
            abort(404)
        return f(*args, **kwargs)
    return function


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)
    return function


# json 中time的格式转化
class Mixin_JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# ajax 返回数据
def ajax_response(valid, data=[], message=''):
    form = {}
    form['message'] = message
    log('data', data)
    if valid:
        form['success'] = True
        form['data'] = data
    else:
        form['success'] = False
    return json.dumps(form, ensure_ascii=False, cls=Mixin_JsonEncoder)


# 判断url 是否属于服务器的域名
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
	ref_url.netloc == test_url.netloc
