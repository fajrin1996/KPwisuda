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

class Panitia(db.Model):
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class namaMahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    npm = db.Column(db.String(40), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    syarat = db.relationship('syaratWis', backref='wisuda', lazy=True)
    prodId = db.Column(db.Integer, db.ForeignKey('prodi.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class syaratWis(db.Model):
    bebas_ak = db.Column(db.String(50), nullable=False)
    ijazah = db.Column(db.String(50), nullable=False)
    pasfoto = db.Column(db.String(50), nullable=False)
    karker = db.Column(db.String(50), nullable=False)
    ktp = db.Column(db.String(50), nullable=False)
    transnli = db.Column(db.String(50), nullable=False)
    bebaspp = db.Column(db.String(50), nullable=False)
    bbspus = db.Column(db.String(50), nullable=False)
    sfkpp = db.Column(db.String(50), nullable=False)
    mahasiswaId = db.Column(db.Integer, db.ForeignKey('namamahasiswa.id'), nullable=False)

# class Post(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# 
    # def __repr__(self):
        # return f"Post('{self.title}', '{self.date_posted}')"
# 

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
