from flask import render_template, request, jsonify, redirect
from flask_login import current_user, login_user
from app import app, db
from app.forms import markdownform
from app.models import Content, ContentSchema 

content_schema = ContentSchema(many=True)

@app.route('/')
def index():
    try:
        posts = Content.query.filter_by(user_id=1).order_by(Content.id.desc()).all()
        return render_template('index.html', posts = posts )
    except:
        return 'Data could not be queried !!'

@app.route('/post')
def post():
    form = markdownform()
    return render_template('post.html', form=form)

#---------------------------------API TEST-------------------------------------
@app.route('/test', methods = ['GET', 'POST'])
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

@app.route('/fetch')
def test_fetch():
    x = Content.query.all()
    y = content_schema.dump(x)
    return jsonify(y)
#------------------------------------------------------------------------------

@app.route('/submit', methods = ['POST'])
def submit():
    try:
        title = request.form['title']
        content = request.form['pagedown']
        sub  = Content(title = title, content = content)
        db.session.add(sub)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was some problem submitting your post !!!'

@app.route('/read/<int:id>')
def read(id):
    try:
        read_post = Content.query.get_or_404(id)
        return render_template('read.html', disp = read_post)
    except:
        return 'Post cannot be fetched'

@app.route('/delete/<int:id>')
def delete(id):
    try:
        delete_this = Content.query.get_or_404(id)
        db.session.delete(delete_this)
        db.session.commit()
        return redirect('/')
    except:
        return 'Post cannot be deleted'

@app.route('/edit/<int:id>')
def edit(id):
    try:
        form = markdownform()
        change = Content.query.get_or_404(id)
        return render_template('change.html', change = change, form = form)
    except:
        return 'Post cannot be fetched for editing'

@app.route('/editview/<int:id>', methods = ['POST'])
def editview(id):
    try:
        post = Content.query.get_or_404(id)
        title = request.form['title']
        content = request.form['pagedown']
        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was some problem updating the post!!!'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if(request.method == 'POST'):
        username = request.json['username']
        password = request.json['password']
        user_check = User.query.filter_by(username=username).first()
        if user_check is None or not user_check.check_passwd(password):
            return 'Invalid credentials'
        login_user(user_check)
        return 'Successfully Logged in'
    return 'Login Form'




