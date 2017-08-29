from flask import Blueprint

simple = Blueprint('simple', __name__, template_folder='templates')

@simple.route('/', methods=['GET'])
def index():
    return 'simple'