from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Concert
import sqlalchemy as sa
from app import db
from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    concert_list = find_latels_concerts(3)
    albums = ['#1', '#2', '#3', '#4']
    return render_template('main/home.html', concert_list=concert_list, albums=albums)


def find_latels_concerts(concert_count=3):
    items = db.session.query(Concert).order_by(
        sa.desc(Concert.date)).limit(concert_count).all()
    concert_list = [
        f"{c.date_str} {c.location[:c.location.find(':')]}" for c in items]
    return concert_list


@bp.route('/bandsite', methods=['GET'])
def show_home_page():
    concert_list = find_latels_concerts()
    albums = ['#1', '#2', '#3', '#4']
    return render_template('main/home.html', concert_list=concert_list, albums=albums)


@bp.route('/bandsite/bandnews', methods=['GET'])
def show_band_news():
    return render_template('main/bandnews.html')


def make_concert_list(page):
    query = sa.select(Concert).order_by(sa.desc(Concert.date))

    concerts = db.paginate(query, page=page, per_page=3, error_out=False)

    next_url = url_for('main.show_concert_list', page=concerts.next_num) \
        if concerts.has_next else None

    prev_url = url_for('main.show_concert_list', page=concerts.prev_num) \
        if concerts.has_prev else None

    ddmm = []
    yy = []
    city = []
    stadium = []

    for elem in concerts.items:
        space_i = elem.date_str.rfind(' ')
        ddmm.append(elem.date_str[:space_i])
        yy.append(elem.date_str[space_i + 1:])

        point_i = elem.location.find(': ')
        city.append(elem.location[:point_i])
        stadium.append(elem.location[point_i + 1:])

    return concerts.items, ddmm, yy, city, stadium, next_url, prev_url


@bp.route('/bandsite/concerts', methods=['GET', 'POST'])
def show_concert_list():
    page = request.args.get('page', 1, type=int)
    items, ddmm, yy, city, stadium, next_url, prev_url = make_concert_list(
        page)
    return render_template('main/concerts.html', concert_list=items, ddmm=ddmm, yy=yy, city=city, stadium=stadium, next_url=next_url, prev_url=prev_url)


@bp.route('/bandsite/music', methods=['GET', 'POST'])
def show_album_list():
    return render_template('main/music.html')


@bp.route('/shop', methods=['GET'])
@login_required
def show_shop_page():
    return render_template('main/shop.html')


@bp.route('/buy_ticket/<concert_id>', methods=['GET', 'POST'])
@login_required
def buy_ticket(concert_id):
    user = db.session.query(User).filter(
        User.username == current_user.username).first()
    if user.concerts_to_visit is None:
        user.concerts_to_visit = str(concert_id)
    elif str(concert_id) not in user.concerts_to_visit:
        user.concerts_to_visit = user.concerts_to_visit + ' ' + str(concert_id)
    db.session.commit()
    return redirect(url_for('auth.user_profile'))
