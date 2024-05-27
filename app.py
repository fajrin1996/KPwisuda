from flask import Flask, render_template, make_response, session, request, redirect, url_for, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import  current_user, LoginManager, logout_user, login_required, UserMixin, login_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import pdfkit



dbuser = 'root'
dbpass ='myPassword' 
dbhost = 'localhost'
dbname = 'kpprojek'
conn = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jkwxv4y'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config["CLIENT_PDF"] = "/home/fajrin/webdev/projekKP/static/formulir/"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
  return Registrasi.query.get(int(user_id))
  

class Fakultas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaFak = db.Column(db.String(20), unique=True, nullable=False)
    prodi =  db.relationship('Prodi', backref='prodi', lazy=True)

class Prodi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaFak = db.Column(db.String(20), nullable=False)
    fakulId = db.Column(db.Integer, db.ForeignKey('fakultas.id'), nullable=False)
    namamhs = db.relationship('Registrasi', backref='nama', lazy=True)

class Panitia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Registrasi(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    npm = db.Column(db.String(40), nullable=False, unique=True ,default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    notif = db.relationship('Notifikasi', backref='author', lazy=True)
    syarat = db.relationship('Wisuda', backref='wisuda', lazy=True)
    prodId = db.Column(db.Integer, db.ForeignKey('prodi.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Wisuda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bebas_ak = db.Column(db.String(50), nullable=False)
    ijazah = db.Column(db.String(50), nullable=False)
    pasfoto = db.Column(db.String(50), nullable=False)
    karker = db.Column(db.String(50), nullable=False)
    ktp = db.Column(db.String(50), nullable=False)
    transnli = db.Column(db.String(50), nullable=False)
    bebaspp = db.Column(db.String(50), nullable=False)
    bbspus = db.Column(db.String(50), nullable=False)
    sfkpp = db.Column(db.String(50), nullable=False)
    verify = db.Column(db.Boolean, default=False)
    mahasiswaId = db.Column(db.Integer, db.ForeignKey('registrasi.id'), nullable=False)
# 
class Notifikasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('registrasi.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# 
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/download-form-wisuda')
# def download():
    # try:
        # return send_from_directory('/home/fajrin/webdev/projekKP/static/formulir/', filename='form-wisuda.pdf', as_attachment=True)
    # except FileNotFoundError:
    #   abort((404))

@app.route('/registrasi-biodata',  methods=['GET', 'POST'])
def reg_bio():

    if request.method == "POST":
        hash_pass = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
        reg = Registrasi(username = request.form['username'], email = request.form['email'] ,npm = request.form['npm'], prodId=1 , password=hash_pass)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('login_mhs'))
    return render_template('reg-biodata.html')

app.route('/test')
def test(nama):
    return f'Hai'

@app.route('/login-panitia', methods=['GET', 'POST'])
def login_pnt():
    if request.method == 'POST':
        pnt = Panitia.query.filter_by(email=request.form.get('email')).first()
        if pnt and bcrypt.check_password_hash(pnt.password, request.form.get('password')):
            session['email'] = request.form.get('email')
            return redirect(url_for('page_panitia'))
    return render_template('login-panitia.html')

@app.route('/logout-panitia')
def logout_panitia():
    session.pop('email')
    return redirect(url_for('login_pnt'))

@app.route('/upload-berkas')
@login_required
def upload_berkas():
    return render_template('upload-berkas.html')

@app.route('/login-mahasiswa', methods=['GET', 'POST'])
def login_mhs():
  if request.method == "POST":
        user = Registrasi.query.filter_by(npm=request.form['npm']).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
          login_user(user)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for("upload_berkas"))
        else:
            print("login gagal harap periksa password dan npm","danger")
  return render_template('login-mhs.html')

@app.route('/logout-mhs')
def logout_mhs():
    logout_user()
    return redirect(url_for('login_mhs'))

if __name__ == '__main__':
    app.run(debug=True)
