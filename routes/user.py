from models.user import User
from routes import *
from utils import current_user, login_required

main = Blueprint('user', __name__)

Model = User


@main.route('/')
def index():
    u = current_user()
    if u is not None:
        return redirect('/weibo')
    return render_template('user/user_index.html')


@main.route('/logout')
@login_required
def logout():
    u = current_user()
    session.pop('uid')
    return redirect(url_for('.index'))


@main.route('/profile/change', methods=['GET','POST'])
def profile_change():
    form = request.form
    u = current_user()
    if u is not None and is_submitted(form):
        u.profile = form.get('profile')
        u.save()
        return redirect(url_for('.profile'))
    return render_template('user/profile_change.html')


@main.route('/profile')
def profile():
    u = current_user()
    if u is not None:
        profile = u.profile
        return render_template('user/profile.html', profile=profile, username=u.username,
                               id=u.id)
    return redirect(url_for('.index'))
