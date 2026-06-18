from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..forms import LoginForm
from ..models import User
from .. import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    print("=" * 50)
    print("REQUEST METHOD:", request.method)

    if request.method == "POST":
        print("FORM DATA:", request.form)
        print("FORM ERRORS:", form.errors)

    if form.validate_on_submit():
        print("FORM VALIDATED")

        user = User.query.filter_by(email=form.email.data).first()
        print("USER FOUND:", user)

        if user:
            password_match = bcrypt.check_password_hash(
                user.password_hash,
                form.password.data
            )
            print("PASSWORD MATCH:", password_match)

            if password_match:
                print("LOGIN SUCCESS")
                login_user(user)
                return redirect(url_for('main.dashboard'))

        flash('Invalid email or password.', 'danger')
    else:
        if request.method == "POST":
            print("FORM VALIDATION FAILED")

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))