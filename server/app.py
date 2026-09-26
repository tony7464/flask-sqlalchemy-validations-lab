from html import escape

from flask import Flask
from flask_migrate import Migrate

from models import db, Author, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    """Show the editorial rules and the records that passed model validation."""
    authors = Author.query.order_by(Author.name).all()
    posts = Post.query.order_by(Post.id).all()

    author_rows = "\n".join(
        f"<li>{escape(author.name)} — {escape(author.phone_number)}</li>"
        for author in authors
    )
    post_rows = "\n".join(
        f"<li>{escape(post.title)} ({escape(post.category)})</li>" for post in posts
    )

    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Editorial Blog — Validations</title>
        <style>
          html {{ color-scheme: light; }}
          body {{
            font-family: Georgia, serif;
            margin: 2rem auto;
            max-width: 42rem;
            background: #fafaf9;
            color: #1c1917;
          }}
          h1 {{ font-size: 1.8rem; }}
          h2 {{ font-size: 1.15rem; margin-top: 1.5rem; }}
          ul {{ line-height: 1.5; }}
          .rules {{ background: #ffffff; padding: 0.75rem 1.25rem; border: 1px solid #e7e5e4; }}
        </style>
      </head>
      <body>
        <h1>Editorial Blog</h1>
        <p>Author and post records are checked in the models before they are saved.</p>
        <h2>Validation rules</h2>
        <ul class="rules">
          <li>Every author has a name, and that name is unique.</li>
          <li>Author phone numbers are exactly ten digits.</li>
          <li>Post content is at least 250 characters.</li>
          <li>Post summaries are at most 250 characters.</li>
          <li>Post category is Fiction or Non-Fiction.</li>
          <li>Post titles include Won't Believe, Secret, Top, or Guess.</li>
        </ul>
        <h2>Authors ({len(authors)})</h2>
        <ul>{author_rows}</ul>
        <h2>Posts ({len(posts)})</h2>
        <ul>{post_rows}</ul>
      </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5555, debug=True)