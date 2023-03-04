from flask import Flask, request, send_from_directory
from database import Database

app = Flask(__name__, static_url_path='', static_folder='static')
db = Database()

if app.debug:
    # pip install flask-cors
    from flask_cors import CORS
    CORS(app)

@app.route("/grep")
def grep():
    term = request.args.get('q')
    results = db.grep(term)
    return [res.to_dict() for res in results]

@app.route("/", defaults={'path':''})
def root(path):
    return send_from_directory(app.static_folder,'index.html')
