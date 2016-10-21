from flask import Blueprint, render_template, redirect, request
from models.weibo import Weibo
from models.weiboComment import WeiboComment
from utils import current_user, login_required

main = Blueprint('weibo', __name__)


@main.route('/')
@login_required
def index():
    weibos = Weibo.query.order_by(Weibo.create_time.desc()).all()
    u = current_user()
    return render_template('/weibo/weibo.html', weibos=weibos, u=u)
