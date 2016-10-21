from models.user import User
from routes import *
from utils import current_user, login_required,log

main = Blueprint('user', __name__)

Model = User


@main.route('/')
def index():
    u = current_user()
    if u is not None:
        return redirect('/weibo')
    return render_template('user/user_index.html', next=request.referrer)


@main.route('/logout')
@login_required
def logout():
    u = current_user()
    session.pop('uid')
    return redirect(url_for('.index'))


@main.route('/profile/change', methods=['POST'])
@login_required
def profile_change():
    form = request.form
    u = current_user()
    u.profile = form.get('profile','')
    u.save()
    return render_template('user/profile_change.html')


@main.route('/profile')
@login_required
def profile():
    u = current_user()
    return render_template('user/profile.html', u=u)
