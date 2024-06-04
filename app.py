from flask import Flask, render_template, make_response, session, request, redirect, url_for, \
      abort, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import  current_user, LoginManager, logout_user, login_required, UserMixin, login_user
from flask_bcrypt import Bcrypt
from datetime import datetime
# from form import Wisudaform
import os
# from werkzeug

dbuser = 'root'
dbpass ='dh1yaL_D' 
dbhost = 'localhost'
dbname = 'kpprojek'
conn = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jkwxv4y'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config["CLIENT_PDF"] = "static/formulir/form-wisuda.pdf"
app.config["DOWNLOAD_PDF"] = 'static/pdf'
app.config['UPLOAD_PDF'] = "static/pdf"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
  return Registrasi.query.get(int(user_id))

pdfpath = 'pdf/'
def makedir(nama):
    if os.path.exists(pdfpath+nama):
        print('the folder is exist')
        return pdfpath+nama
    else:
        os.makedirs(pdfpath+nama)
    return pdfpath+nama
# 
def auto_fol(nama):
    return nama

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
    syarat = db.relationship('Wisuda', backref='wsd', lazy=True)
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

    def __repr__(self):
        return f"Wisuda('{self.bebas_ak}', '{self.ijazah}', '{self.pasfoto}', '{self.karker}', '{self.ktp}', \
            '{self.transnli}', '{self.bebaspp}', '{self.bbspus}', '{self.sfkpp}', '{self.mahasiswaId}')"

class Notifikasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('registrasi.id'), nullable=False)

    def __repr__(self):
        return f"Notifikasi('{self.date_posted}', '{self.content}','{self.user_id})"

 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download-form-wisuda')
def download():
    try:
        return send_file(app.config["CLIENT_PDF"], as_attachment=True)
    except FileNotFoundError:
      abort((404))

@app.route('/registrasi-biodata',  methods=['GET', 'POST'])
def reg_bio():
    prodi = Prodi.query.all()
    if request.method == "POST":
        hash_pass = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
        reg = Registrasi(username = request.form['username'], email = request.form['email'] ,npm = request.form['npm'], prodId=1 , password=hash_pass)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('login_mhs'))
    return render_template('reg-biodata.html', prodi=prodi)

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

@app.route('/page-panitia')
def page_panitia():
    return render_template('page_panitia.html')


#makedir(current_user.npm),
@app.route('/upload-berkas', methods=['GET', 'POST'])
@login_required
def upload_berkas():
    if request.method == "POST":
        bebas_ak = request.files['akademik']
        ijazah = request.files['ijazah']
        pasfoto = request.files['pasfoto']
        karker = request.files['karker']
        ktp = request.files['ktp']
        transnli =  request.files['transnli']
        bebaspp = request.files['bebaspp']
        bbspus = request.files['bbspus']
        sfkpp = request.files['sfkpp']
    
        bebas_ak.save(os.path.join(app.config['UPLOAD_PDF'],bebas_ak.filename))
        ijazah.save( os.path.join(app.config['UPLOAD_PDF'],  ijazah.filename))
        bbspus.save(os.path.join(app.config['UPLOAD_PDF'], bbspus.filename) )
        bebaspp.save(os.path.join(app.config['UPLOAD_PDF'],  bebaspp.filename))
        karker.save(os.path.join(app.config['UPLOAD_PDF'],  karker.filename))
        pasfoto.save(os.path.join(app.config['UPLOAD_PDF'],  pasfoto.filename))
        ktp.save(os.path.join(app.config['UPLOAD_PDF'],  ktp.filename))
        transnli.save(os.path.join(app.config['UPLOAD_PDF'],  transnli.filename))
        sfkpp.save(os.path.join(app.config['UPLOAD_PDF'], sfkpp.filename))

        
        syarat = Wisuda( bebas_ak=bebas_ak.filename, ijazah=ijazah.filename,\
                         pasfoto=pasfoto.filename, karker=karker.filename, \
                        ktp=ktp.filename, 
                         transnli=transnli.filename, bebaspp=bebaspp.filename,\
                          bbspus=bbspus.filename, sfkpp=sfkpp.filename, mahasiswaId=current_user.id)
 
        db.session.add(syarat)
        db.session.commit()


        print('berhasil disimpan')
        return redirect(url_for('page_mhs'))
    return render_template('upload-berkas.html')

@app.route('/login-mahasiswa', methods=['GET', 'POST'])
def login_mhs():
  if request.method == "POST":
        user = Registrasi.query.filter_by(npm=request.form['npm']).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
          login_user(user)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for("page_mhs"))
        else:
            print("login gagal harap periksa password dan npm","danger")
  return render_template('login-mhs.html')

@app.route('/page-mahasiswa')
@login_required
def page_mhs():
    wsd = Wisuda.query.filter_by(mahasiswaId=current_user.id).first()
    return render_template('page-mahasiswa.html', wsd=wsd)

@app.route('/laman-validasi-mahasiswa')
def daftar_mhs():
    if session.get('email'):
        valid = db.session.query(Registrasi.email, Registrasi.username, Registrasi.npm, Prodi.namaFak, Wisuda.mahasiswaId).join(Wisuda, Registrasi.id == Wisuda.mahasiswaId)\
            .join(Prodi, Registrasi.prodId == Prodi.id).filter(Wisuda.verify == 0).all()
        return render_template('daftar-val-mahasiswa.html', valid=valid)
    else:
        return redirect(url_for('login_pnt'))

@app.route('/laman-periksa-dokumen/<int:ids>') 
def periksa_dok(ids):
     if session.get('email'):
        nama = Wisuda.query.filter(Wisuda.mahasiswaId==ids).first()
        return render_template('periksa-dok.html', nama=nama)
     else:
        return redirect(url_for('login_pnt'))
    
@app.route('/lolos-verifikasi/<int:ids>')
def lolos_ver(ids):
    if session.get('email'):
        wsda = Wisuda.query.filter(Wisuda.mahasiswaId==ids).first()
        wsda.verify = 1
        db.session.commit()
        return redirect(url_for('daftar_mhs'))
    else:
        return redirect(url_for('login_pnt'))
    
@app.route('/download-berkas-wisuda/<filename>')
def download_wsd(filename):
    try:
        return send_from_directory(app.config["DOWNLOAD_PDF"], path=filename, as_attachment=True)

    except FileNotFoundError:
            abort((404))

@app.route('/logout-mhs')
def logout_mhs():
    logout_user()
    return redirect(url_for('login_mhs'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
