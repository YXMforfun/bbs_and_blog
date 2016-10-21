from flask import Blueprint, request
from models.weibo import Weibo
from models.weiboComment import WeiboComment
from utils import current_user, ajax_response, log, login_required
from datetime import datetime

main = Blueprint('api_weibo', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add_weibo():
    u = current_user()
    form = request.form
    w = Weibo(form)
    valid, message = w.valid()
    if valid:
        w.author_id = u.id
        w.save()
    return ajax_response(valid=valid, data=w.json(), message=message)


@main.route('/delete/<int:weibo_id>')
@login_required
def delete_weibo(weibo_id):
    u = current_user()
    w = Weibo.query.get(weibo_id)
    is_auth, message = w.is_auth(u)
    if is_auth:
        w.delete()
    return ajax_response(is_auth, data=w.json(), message=message)


@main.route('/update/<int:weibo_id>', methods=['POST'])
@login_required
def update_weibo(weibo_id):
    u = current_user()
    w = Weibo.query.get(weibo_id)
    form = request.form
    is_auth, message = w.is_auth(u)
    if is_auth:
        w.body = form.body
        w.save()
    return ajax_response(is_auth, data=w.json(), message=message)


@main.route('/get/<int:weibo_id>')
@login_required
def get_weibo(weibo_id):
    w = Weibo.query.get(weibo_id)
    return ajax_response(True, data=w.json())


@main.route('/<int:weibo_id>/comment')
@login_required
def weibo_comment(weibo_id):
    w = Weibo.query.get(weibo_id)
    comments = [c.json() for c in w.comment]
    return ajax_response(True, data=comments)


@main.route('/comment/add', methods=['POST'])
@login_required
def add_comment():
    u = current_user()
    form = request.form
    c = WeiboComment(form)
    valid, message = c.valid()
    if valid:
        c.weibo_id = int(form.get('weibo_id', -1))
        c.author_id = u.id
        c.save()
    return ajax_response(True, data=c.json(), message=message)


@main.route('/comment/<int:comment_id>')
@login_required
def get_comment(comment_id):
    c = WeiboComment.query.get(comment_id)
    return ajax_response(True, data=c.json())


@main.route('/comment/update/<int:comment_id>', methods=['POST'])
@login_required
def update_comment(comment_id):
    u = current_user()
    form = request.form
    c = WeiboComment.query.get(comment_id)
    is_auth, message = c.is_auth(u)
    if is_auth:
        c.body = form.get('body','')
        c.update_time = datetime.utcnow()
        c.save()
    return ajax_response(is_auth, data=c.json(), message=message)


@main.route('/comment/delete/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    u = current_user()
    c = WeiboComment.query.get(comment_id)
    is_auth, message = c.is_auth(u)
    if is_auth:
        c.delete()
    return ajax_response(is_auth, data=c.json(), message=message)
