from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr_codes.db'

db = SQLAlchemy(app)

class QRCodes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    qr_data = db.Column(db.String(255))

    def __init__(self, qr_data):
        self.qr_data = qr_data

@app.route('/', methods=['GET'])
def serve_index():
    return render_template('index.html')

@app.route('/random', methods = ['POST'])
def save_qr_code():
    web_url = request.json.get('qrdata')
    data = QRCodes(web_url)
    db.session.add(data)
    db.session.commit()
    return jsonify({"message": "Data received", "qrdata": web_url}), 200

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug = True)