from routes import *


main = Blueprint('home', __name__)


@main.route('/')
def index():
    return render_template('home/index.html')