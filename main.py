from flask import Flask
from flask import render_template
from flask_cors import CORS

from report import views as report_views
from data import views as data_views
import simple

app = Flask(__name__)

app.register_blueprint(report_views.bp, url_prefix='/reports')
app.register_blueprint(simple.simple, url_prefix='/simple')
app.register_blueprint(data_views.bp, url_prefix='/data')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

print(app.url_map)