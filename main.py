from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager
from forms import CreateAccForm, LogInForm
from flask_login import LoginManager, UserMixin, login_required, login_user


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubah/Documents/Pyyy/NewSite/band.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


db = SQLAlchemy(app)
#manager = Manager(app)
#db.init_app(app)


class Concert(db.Model):
    __tablename__ = 'concerts'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)
    tickets_left = db.Column(db.Integer())

    def __repr__(self):
        return f"{self.id} {self.date}"
    

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def index():
    items = db.session.query(Concert).limit(3).all()
    concert_list = [f"{c.date} {c.location[:c.location.find(':')]}" for c in items]

    albums = ['#1', '#2', '#3', '#4']
    
    return render_template('home.html', concert_list=concert_list, albums=albums)


@app.route('/bandnews')
def bandpage():
    return render_template('bandnews.html')


@app.route('/concerts', methods=['GET', 'POST'])
def concertspage():
    items = []
    ddmm = []
    yy = []
    city = []
    stadium = []

    if request.method == 'GET':
        alb_count = 0
        if request.cookies.get('alb_count') == None:
            alb_count = 3
        else:
            alb_count = int(request.cookies.get('alb_count'))

        items = db.session.query(Concert).limit(alb_count).all()
        for elem in items:
            space_i = elem.date.rfind(' ')
            ddmm.append(elem.date[:space_i])
            yy.append(elem.date[space_i + 1:])
            
            point_i = elem.location.find(': ')
            city.append(elem.location[:point_i])
            stadium.append(elem.location[point_i + 1:])
        
    elif request.method == 'POST':
        if request.cookies.get('alb_count') == None:
            alb_count = 6
        else:
            alb_count = int(request.cookies.get('alb_count')) + 3
        
        res = make_response("")
        res.set_cookie('alb_count', str(alb_count), 60*5)
        res.headers['location'] = url_for('concertspage')
        return res, 302
    
    return render_template('concerts.html', concert_list=items, ddmm=ddmm, yy=yy, city=city, stadium=stadium)


@app.route('/music')
def musicpage():
    return render_template('music.html')


@app.route('/shop', methods=['GET', 'POST'])
@login_required
def shoppage():
    return render_template('shop.html')


@app.route('/create-acc', methods=['GET', 'POST'])
def create_acc():
    form = CreateAccForm()
    if form.validate_on_submit():
        name = form.name.data
        passwrd = form.password.data
        email = form.email.data
        user = User(username=name, email=email)
        user.set_password(passwrd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('shoppage'))
    
    return render_template('contact.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('shoppage'))
        else:
            return redirect(url_for('login'))
        
    return render_template('login.html', form=form)


if __name__ == "__main__":
    #manager.run()
    with app.app_context():
        db.create_all()
    app.run(debug=True)