from flask import render_template, request, jsonify, redirect
from flask_login import current_user, login_user, login_required
from app import app, db
from app.forms import markdownform, LoginForm
from app.models import Content, ContentSchema 

content_schema = ContentSchema(many=True)

@app.route('/')
@login_required
def index():
    try:
        posts = Content.query.filter_by(user_id=current_user.id).order_by(Content.id.desc()).all()
        return render_template('index.html', posts = posts )
    except:
        return 'Data could not be queried !!'


@app.route('/post')
@login_required
def post():
    form = markdownform()
    if form.validate_on_submit():
        try:
            title = request.form['title']
            content = request.form['pagedown']
            sub  = Content(title = title, content = content)
            db.session.add(sub)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was some problem submitting your post !!!'

    return render_template('post.html', form=form)

#---------------------------------API TEST-------------------------------------
@app.route('/test_send', methods = ['GET', 'POST'])
def test_send():
    title = request.json['title']
    content = request.json['content']
    try:
        add_this = Content(title = title, content = content )
        db.session.add(add_this)
        db.session.commit()
        return 'Success!'
    except:
        return 'There was some problem!!'

@app.route('/test_fetch')
def test_fetch():
    x = Content.query.all()
    y = content_schema.dump(x)
    return jsonify(y)
#------------------------------------------------------------------------------


@app.route('/read/<int:id>')
@login_required 
def read(id):
    try:
        read_post = Content.query.get_or_404(id)
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
            return redirect('/')
        change = Content.query.get_or_404(id)
        return render_template('change.html', change = change, form = form)
    except:
        return 'Post cannot be fetched for editing'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        prob_user = User.query.filter_by(username=form.username.data).first()
        if prob_user is None or prob_user.check_passwd(form.username.data) is False:
            flash('Invalid login')
            return redirect('/login')
        
    return render_template('login.html', form = form)
