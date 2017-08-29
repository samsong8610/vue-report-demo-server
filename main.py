from flask import Flask
from flask_cors import CORS

from report import views as report_views
import simple

app = Flask(__name__)

app.register_blueprint(report_views.bp, url_prefix='/reports')
app.register_blueprint(simple.simple, url_prefix='/simple')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "index page"

print(app.url_map)