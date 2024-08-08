from app import db
from app.auth import bp
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, Concert
from app.auth.forms import LogInForm, CreateAccForm, ResetPasswordRequestForm, ResetPasswordForm, LogoutButton
from app.auth.email import send_password_reset_email


@bp.route('/create-acc', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.show_shop_page'))
    form = CreateAccForm()
    if form.validate_on_submit():
        name = form.name.data
        passwrd = form.password.data
        email = form.email.data
        user = User(username=name, email=email)
        user.set_password(passwrd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/contact.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.username == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('auth.user_profile'))
        else:
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('user-profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = LogoutButton()
    if form.validate_on_submit():
        return redirect(url_for('auth.logout'))
    user = db.session.query(User).filter(User.id == current_user.id).first()
    user_next_concerts = (int(concert_id)
                          for concert_id in user.concerts_to_visit.split(' '))
    concert_items = db.session.query(Concert).filter(
        Concert.id.in_(user_next_concerts))

    return render_template('auth/profile.html', form=form, concert_items=concert_items)
