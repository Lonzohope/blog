from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import  CommentForm, BlogForm
from ..models import User, Blog, Comment
from flask_login import login_required,current_user
from datetime import datetime
import markdown2
from ..requests import get_quotes


# Views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    myquote = get_quotes()
    quote = myquote['quote']
    quote_author = myquote['author']
    page = request.args.get('page', 1, type=int)

    title = 'Home | Art'
    all_blogs = Blog.get_all_blogs()

    if all_blogs:
        blogs = all_blogs
        return render_template('index.html', title=title, all_blogs=blogs, subscribe_form = form,quote = quote,quote_author = quote_author)
    elif not all_blogs:
        blog_message = 'Whoooops, we have no blogs here'
    
    
    return render_template('index.html', title=title, blog_message = blog_message, subscribe_form = form,quote = quote,quote_author = quote_author)


    

@main.route('/blog/<int:id>', methods=['GET','POST'])
def blog(id):
    get_blog = Blog.query.get(id)
    get_blog_comments = Comment.get_blog_comments(id)

    if get_blog is None:
        abort(404)

    blog_format = markdown2.markdown(get_blog.blog_content,extras=["code-friendly", "fenced-code-blocks"])

    comment_form = CommentForm()

      if comment_form.validate_on_submit():
        user_name = comment_form.name.data
        user_comment = comment_form.comment_data.data

        new_comment = Comment(name=user_name,email=user_email,comment_content=user_comment,date_comment = datetime.now(),blog_id=id)
        new_comment.save_comment()

        return redirect(url_for('main.blog',id=id))
    
    get_comments = Comment.get_blog_comments(id)

    return render_template('blog.html', blog_format=blog_format, get_blog=get_blog, title="Blog", comment_form=comment_form, get_comments=get_comments, comments_count = len(get_blog_comments))



@main.route('/create_blog', methods = ['GET','POST'])
@login_required
def create_blog():
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        blog_title = blog_form.title.data
        blog = blog_form.blog_data.data
        url = blog_form.photo_url.data

        new_blog = Blog(title=blog_title, blog_content = blog, date_posted = datetime.now(), photo_url=url)
        new_blog.save_blog()

        return redirect(url_for('main.blog',id=new_blog.id))

    return render_template('create_blog.html', title = 'Create Blog', blog_form = blog_form)


@main.route('/abstract', methods=['GET','POST'])
@login_required
def abstract(category = "Abstract"):

    abstract = Blog.query.filter_by(category = "Abstract")
    
    title = "Abstract Blogs"
    return render_template('abstract.html', abstract= abstract, title=title, blog ='Create Blog')





@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

 @main.route('/blog/<int:id>/<int:id_comment>/delete_comment')
@login_required
def delete_comment(id,id_comment):
    comment = Comment.get_single_comment(id,id_comment)

    db.session.delete(comment)
    db.session.commit()


    return redirect(url_for('main.blog',id=id))


@main.route('/index/<int:id>/delete_blog')
@login_required
def delete_blog(id):
    blog = Blog.get_single_blog(id)

    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.index'))

