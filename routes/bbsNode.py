from routes import *
from utils import admin_required, login_required, current_user
from models.bbsTag import bbsTag
from models.bbsNode import bbsNode
from models.bbsContent import bbsContent


main = Blueprint("bbs_node", __name__)


@main.route('/')
@login_required
@admin_required
def node_list():
    u = current_user()
    n = bbsNode.query.all()
    return render_template('bbs/node_list.html', nodes=n, u=u)


@main.route('/<int:id>')
@login_required
@admin_required
def node_get(id):
    u = current_user()
    n = bbsNode.query.get(id)
    return render_template('bbs/node_show.html', node=n, u=u)


@main.route('/add', methods=['POST'])
@login_required
@admin_required
def node_add():
    form = request.form
    n = bbsNode(form)
    n.save()
    return redirect(url_for('.node_list'))


@main.route('/delete/<int:id>')
@login_required
@admin_required
def node_delete(id):
    n = bbsNode.query.get(id)
    n.delete()
    return redirect(url_for('.node_list'))


@main.route('/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def node_update(id):
    form = request.form
    n = bbsNode.query.get(id)
    n.name = form.get('name', '')
    n.description = form.get('description', '')
    n.save()
    return redirect(url_for('.node_list'))

