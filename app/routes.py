from flask import render_template, request, jsonify, redirect, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db, moment
from app.forms import markdownform, LoginForm, SignUpForm, PasswordResetRequestForm, ResetPasswordForm
from app.models import Content, User
from app.email import send_password_reset_mail
from werkzeug.urls import url_parse
import markdown
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

# OAuth Google.
@app.route('/login_google', methods=['POST', 'GET'])
def login_google():
    pass

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




    
