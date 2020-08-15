from flask import render_template, request, jsonify, redirect
from app import app, db
from app.forms import markdownform
from app.models import Content, ContentSchema 

content_schema = ContentSchema(many=True)

@app.route('/')
def index():
    try:
        data = Content.query.all()
        return render_template('index.html', data = data )
    except:
        return 'Data could not be queried !!'

@app.route('/post')
def post():
    form = markdownform()
    return render_template('post.html', form=form)

@app.route('/test', methods = ['GET', 'POST'])
def test():
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
def fetc():
    x = Content.query.all()
    y = content_schema.dump(x)
    return jsonify(y)

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['pagedown']
            sub  = Content(title = title, content = content)
            db.session.add(sub)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was some problem !!'

@app.route('/read/<int:id>')
def read(id):
    try:
        disp = Content.query.get_or_404(id)
        return render_template('read.html', disp = disp)
    except:
        return 'Post cant be fetched'

@app.route('/delete/<int:id>')
def delete(id):
    try:
        disp = Content.query.get_or_404(id)
        db.session.delete(disp)
        db.session.commit()
        return redirect('/')
    except:
        return 'Post cant be deleted'

@app.route('/putc/<int:id>')
def putc(id):
    try:
        form = markdownform()
        change = Content.query.get_or_404(id)
        return render_template('change.html', change = change, form = form)
    except:
        return 'Post cant be fetched for editing'
