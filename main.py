# İçeri Aktarma
from flask import Flask, render_template, request, redirect
# Veritabanı kütüphanesini içe aktarma
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# SQLite ile bağlantı kurma 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app)

# Görev #1. DB tablosu oluşturma
class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    user = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Card {self.id}>"

# Ödev #2. Kullanıcı tablosunu oluşturun
class Kullanici(db.Model):
    __tablename__ = "kullanicilar"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)


with app.app_context():
    db.create_all()


# Giriş sayfası
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        # Ödev #4. yetkilendirmeyi uygulamak
        user = Kullanici.query.filter_by(login=form_login, password=form_password).first()
        if user:
            return redirect('/index')
        else:
            error = 'Hatalı Giriş veya Şifre'
        return render_template('login.html', error=error)

    return render_template('login.html')


# Kayıt sayfası
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']

        # Ödev #3 Kullanıcı verilerinin veri tabanına kaydedilmesini sağlayın
        kullanici = Kullanici(login=login, password=password)
        db.session.add(kullanici)
        db.session.commit()

        return redirect('/')
    return render_template('registration.html')


# İçerik sayfası
@app.route('/index')
def index():
    # DB nesnelerini görüntüleme
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)


# Kart detay sayfası
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get_or_404(id)
    return render_template('card.html', card=card)


# Kart oluşturma sayfası
@app.route('/create')
def create():
    return render_template('create_card.html')


# Kart formu
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        user = request.form['user']
        text = request.form['text']
    
        # DB'ye kaydetme
        card = Card(title=title, subtitle=subtitle, text=text, user=user)
        db.session.add(card)
        db.session.commit()

        return redirect('/index')
    return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
