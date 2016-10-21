from api import *
from models.user import User
from utils import ajax_response, log, is_safe_url


main = Blueprint('api_user', __name__)
Model = User

def safe_redirect_ajax(form, json):
        next = form.get('next', '')
        if is_safe_url(next):
            json['next'] = next
        else :
            json['next'] = url_for('bbs_content.content_show', _external=True)


@main.route('/check/username', methods=['POST'])
def check_name():
    form = request.form
    u = Model(form)
    valid, message = u.valid_username()
    return ajax_response(valid=valid, message=message)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = Model(form)
    valid, message = u.valid()
    json = u.json()
    if valid:
        u.save()
        session['uid'] = u.id
        safe_redirect_ajax(form, json)
    return ajax_response(valid=valid, data=json, message=message)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user = Model.query.filter_by(username=u.username).first()
    valid, message = u.valid_login(user)
    json = u.json()
    if valid:
        session['uid'] = user.id
        safe_redirect_ajax(form, json)
    return ajax_response(valid=valid, data=json, message=message)


@main.route('/<int:user_id>')
def get_user(user_id):
    u = Model.query.get(user_id)
    return ajax_response(valid=True, data=u.json())
