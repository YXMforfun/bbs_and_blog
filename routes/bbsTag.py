from routes import *
from utils import admin_required, login_required, current_user
from models.bbsTag import bbsTag



main = Blueprint("bbs_Tag", __name__)


@main.route('/')
def tag_show():
    u = current_user()
    t = bbsTag.query.all()
    return render_template('bbs/tag_show.html', tags=t, u=u)


@main.route('/<int:id>')
def tag_get(id):
    u = current_user()
    t = bbsTag.query.get(id)
    return render_template('bbs/tag_show.html', tags=t,u=u)


@main.route('/add', methods=['POST'])
@login_required
@admin_required
def tag_add():
    form = request.form
    t = bbsTag(form)
    t.add_node(form)
    t.save()
    return redirect(url_for('.tag_show'))


@main.route('/delete/<int:id>')
@login_required
@admin_required
def tag_delete(id):
    t = bbsTag.query.get(id)
    t.delete()
    return redirect(url_for('.tag_show'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def tag_update(id):
    form = request.form
    t = bbsTag.query.get(id)
    t.update(form)
    t.save()
    return redirect(url_for('.tag_show'))