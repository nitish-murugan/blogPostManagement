from flask import Blueprint,render_template,request,flash,redirect,url_for,current_app
from flask_login import login_required,current_user
from .model import Post,User,Comment
from werkzeug.utils import secure_filename
import os
import base64
from . import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

view = Blueprint("view",__name__)

@view.route('/')
@view.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user,posts=posts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view.route('/createPost',methods=['GET','POST'])
@login_required
def createPost():
    if request.method == 'POST':
        text = request.form.get('text')
        file = request.files['upload']
        flag = True
        if file and file.filename:
            filename = secure_filename(file.filename)
            extension = os.path.splitext(filename)[1]
        if not text:
            flash("Post cannot be empty",category="error")
        else:
            post = Post(text=text,author=current_user.id,photoLocation="")
            db.session.add(post)
            db.session.commit()
            db.session.flush()
            photo_location = f"{post.id}{extension}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_location))
            post.photoLocation = photo_location
            db.session.commit()
            flash("post created",category="success")
            return redirect(url_for("view.home"))
    return render_template('createPost.html',user=current_user)

@view.route("/deletePost/<id>")
@login_required
def deletePost(id):
    post = Post.query.filter_by(id=id).first()
    commentIds = [comment.id for comment in post.comments]
    print(commentIds)
    if not post:
        flash("Post isn't available",category='error')
    elif current_user.id != post.author:
        flash("You don't have permission to delete the post",category='error')
    else:
        flash("Post deleted",category='success')
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('view.home'))

@view.route("/post/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Post.query.filter_by(author=user.id).all()
        return render_template("post.html",user=current_user,posts=posts,username=username)
    else:
        flash("User doesn't exist",category="error")
        return redirect(url_for('view.home'))

@view.route("/createComment/<postId>", methods=["POST"])
@login_required
def createComment(postId):
    text = request.form.get('text')
    if not text:
        flash("Comment cannot be empty",category="error")
    else:
        post = Post.query.filter_by(id=postId).first()
        if not post:
            flash("Post doesn't exists",category="error")
        else:
            comment = Comment(text=text,author=current_user.id,post=post)
            db.session.add(comment)
            db.session.commit()
    return redirect(url_for("view.home"))

@view.route("/deleteComment/<commentId>")
@login_required
def deleteComment(commentId):
    comment = Comment.query.filter_by(id=commentId).first()
    if not comment:
        flash("Comment not available",category="error")
    elif current_user.id != comment.author:
        flash("You don't have access to delete the comment",category="error")
    else:
        flash("Comment deleted",category="success")
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for("view.home"))