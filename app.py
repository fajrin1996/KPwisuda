from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


db = SQLAlchemy()
class Fakultas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaFak = db.Column(db.String(20), unique=True, nullable=False)
    prodi =  db.relationship('Prodi', backref='prodi', lazy=True)

class Prodi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaFak = db.Column(db.String(20), nullable=False)
    fakulId = db.Column(db.Integer, db.ForeignKey('fakultas.id'), nullable=False)
    namaMHS = db.relationship('namaMahasiswa', backref='nama', lazy=True)

class namaMahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    npm = db.Column(db.String(40), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    prodId = db.Column(db.Integer, db.ForeignKey('prodi.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
