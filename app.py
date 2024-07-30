from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
import re
from datetime import datetime
from models import db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/trips.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Username already exists.', 'danger')
        elif existing_email:
            flash('Email already registered.', 'danger')
        elif not is_valid_email(email):
            flash('Invalid email format.', 'danger')
        elif not is_valid_password(password):
            flash('Password must be at least 8 characters long and contain both letters and numbers.', 'danger')
        else:
            new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_post = Post(image_file=filename, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash('Your photo has been uploaded!', 'success')
            return redirect(url_for('feed'))
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/feed')
@login_required
def feed():
    posts = current_user.followed_posts().all()
    return render_template('feed.html', posts=posts)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('account'))
    db.session.delete(post)
    db.session.commit()
    flash('Your photo has been deleted', 'success')
    return redirect(url_for('account'))

@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            flash('Username already taken. Please choose another one.', 'danger')
        else:
            current_user.username = new_username
            db.session.commit()
            flash('Your username has been updated.', 'success')
            return redirect(url_for('account'))
    return render_template('change_username.html')

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('feed'))
    if user == current_user:
        flash('You cannot follow yourself.', 'danger')
        return redirect(url_for('feed'))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}.', 'success')
    return redirect(url_for('feed'))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('feed'))
    if user == current_user:
        flash('You cannot unfollow yourself.', 'danger')
        return redirect(url_for('feed'))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {username}.', 'success')
    return redirect(url_for('feed'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q')
    if not query:
        return redirect(url_for('feed'))
    users = User.query.filter(User.username.contains(query)).all()
    return render_template('search_results.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
