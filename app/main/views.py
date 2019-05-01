from flask import render_template,request,redirect,url_for,abort,flash
from ..models import User,Blogs,Comments
from . import main
from flask_login import login_required,current_user
from .forms import UpdateProfile,WritePitch,ReviewForm
from .. import db,photos
@main.route("/")
def index():
    title="Pitch"
    message="Home of ideas, Where ideas are born"
    top=Pitches.query.all();
    pitch=Pitches.query.filter_by(categ="AI").all()
    pitch1=Pitches.query.filter_by(categ="R").all()
    pitch2=Pitches.query.filter_by(categ="D").all()
    pitch3=Pitches.query.filter_by(categ="IOT").all()
    top.reverse()
    top_pitch=top[0:4]
    return render_template("index.html",title=title,message=message,pitch=pitch,top_pitch=top_pitch,pitch1=pitch1,pitch2=pitch2,pitch3=pitch3)


@main.route("/user/<uname>")
def profile(uname):
    user=User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    blog=Blogs.query.filter_by(author=uname).all()
    title=uname
    return render_template("profile/profile.html",user=user,blog=blog,title=title)

'''
new blog idea
'''

@main.route("/<uname>",methods=["GET","POST"])
@login_required
def new_blog(uname):
    uname=uname
    user=User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form=WriteBlog()
    if form.validate_on_submit():
        new_Blog=Blog(Blog=form.blog.data,title=form.title.data,author=uname,categ=form.categ.data)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for(".index"))


    title="new Blog"
    return render_template("blog.html",new_review=form,title=title)

'''
review
'''

@main.route("/blog/new/review/<int:id>",methods=["GET","POST"])
@login_required
def review(id):
    blog_id=id
    blog=Blog.query.all();
    title="Write a comment"
    form=ReviewForm()
    if form.validate_on_submit():
        title=form.title.data
        comments=form.comments.data

        #update this variables
        review=Comments(blog_id=id,blog_title=title,comments=comments,user=current_user)

        #save
        review.save_comment()
        return redirect(url_for('.review',id=blog_id))

    '''
    query Comments database table
    '''
    all_comments=Comments.query.filter_by(blog_id=id).all()

    return render_template("new_review.html",blog=blog,id=blog_id,title=title,comment_form=form,all=all_comments)


@main.route("/user/<uname>/update",methods=["GET","POST"])
@login_required
def update_profile(uname):
    user=User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    form =UpdateProfile()
    if form.validate_on_submit():
        user.about=form.about.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for(".profile",uname=user.username))

    return render_template("profile/update.html",form=form)

'''
update photos
'''
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile= path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

'''
up down vote
'''

def upVote():
    vote=0;


def downVote():
    pass
