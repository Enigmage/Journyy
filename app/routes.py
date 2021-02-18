from flask import render_template, request, jsonify, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db, moment, client
from app.forms import markdownform, LoginForm, SignUpForm, PasswordResetRequestForm, ResetPasswordForm
from app.models import Content, User
from app.email import send_password_reset_mail
from app.utils import get_google_endpoints
from werkzeug.urls import url_parse
import markdown
import requests
import json
import markdown.extensions.fenced_code

@app.route('/index')
@login_required
def index():
    try:
        posts = Content.query.filter_by(user_id=current_user.id).order_by(Content.id.desc()).all()
        return render_template('index.html', posts = posts )
    except:
        return 'Data could not be queried !!'


@app.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    form = markdownform()
    if form.validate_on_submit():
        try:
            title = request.form['title']
            content = request.form['pagedown']
            sub  = Content(title = title, content = content, author=current_user)
            db.session.add(sub)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was some problem submitting your post !!!'

    return render_template('post.html', form=form)

@app.route('/read/<int:id>')
@login_required 
def read(id):
    try:
        read_post = Content.query.get_or_404(id)
        read_post.content = markdown.markdown(read_post.content, extensions=["fenced_code"])
        return render_template('read.html', disp = read_post)
    except:
        return 'Post cannot be fetched'

@app.route('/delete/<int:id>')
@login_required 
def delete(id):
    try:
        delete_this = Content.query.get_or_404(id)
        db.session.delete(delete_this)
        db.session.commit()
        return redirect('/')
    except:
        return 'Post cannot be deleted'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:
        form = markdownform()
        if form.validate_on_submit():
            post = Content.query.get_or_404(id)
            title = request.form['title']
            content = request.form['pagedown']
            post.title = title
            post.content = content
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        change = Content.query.get_or_404(id)
        return render_template('change.html', change = change, form = form)
    except:
        return 'Post cannot be fetched for editing'

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_passwd(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', form = form)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        prob_user = User.query.filter_by(username=form.username.data).first()
        if prob_user is None or not prob_user.check_passwd(form.password.data):
            flash(u'Invalid username or password', 'error')
            return redirect('/login')
        login_user(prob_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # url parse checks if path provided is relative for security reasons.
        # if there is no next page in endpoint, next page becomes index
        # Is not working, its just included for best practise.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/password_reset_request', methods=['POST', 'GET'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_mail(user)
        flash(u'check your email for instructions regarding the password reset', 'message')
        return redirect(url_for('login'))
    return render_template('password_reset_request.html', title = 'Reset password', form = form)

@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user.set_passwd(form.password.data)
        db.session.commit()
        flash(u'The password has been reset !!', 'message')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form = form, token=token)


@app.route('/login_google', methods = ['POST', 'GET'])
def login_google():
    google_endpoints = get_google_endpoints()
    auth_endpoint = google_endpoints['authorization_endpoint']
    request_uri = client.prepare_request_uri( auth_endpoint, 
                                             redirect_uri = f"{request.base_url}/callback",
                                             scope = ["openid", "email", "profile"]
                                             )
    return redirect(request_uri)


@app.route('/login_google/callback', methods = ['POST', 'GET'])
def login_google_callback():
    # Get auth code sent back by google.
    code = request.args.get("code")
    google_endpoints= get_google_endpoints()
    token_endpoint = google_endpoints['token_endpoint']
    # Construct and send token request.
    token_url, header, body = client.prepare_token_request( token_endpoint, 
                                                           authorization_response=request.url,
                                                           redirect_url = request.base_url,
                                                           code = code
                                                           )
    token_response = requests.post(token_url, headers=header, data=body, auth=(app.config['GOOGLE_CLIENT_ID'],
                                                                               app.config['GOOGLE_CLIENT_SECRET']),
                                   )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_endpoints['userinfo_endpoint']
    uri, header, body  = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=header, data=body)
    if userinfo_response.json().get("email_verified"):
        uid = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        user_name = userinfo_response.json()["given_name"]
        user = User.query.filter_by(social_id = uid).first()
        if not user:
            add_user = User(social_id = uid, username=user_name, email=user_email)
            db.session.add(add_user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    else:
        return "The user cannot be verified by google !!"


