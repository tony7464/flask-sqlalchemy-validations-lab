from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        """Require a name, and reject a name already stored for another author."""
        if not name:
            raise ValueError("Author must have a name.")

        # Skip autoflush so this lookup does not persist the author being created.
        with db.session.no_autoflush:
            existing_author = db.session.query(Author).filter(Author.name == name).first()

        if existing_author is not None and existing_author.id != self.id:
            raise ValueError("Author name must be unique.")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        """Require a phone number of exactly ten numeric digits."""
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Author phone number must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Clickbait phrases the editorial team requires in every title.
    CLICKBAIT_PHRASES = ("Won't Believe", "Secret", "Top", "Guess")
    ALLOWED_CATEGORIES = ("Fiction", "Non-Fiction")

    @validates('title')
    def validate_title(self, key, title):
        """Require a non-empty title that includes at least one clickbait phrase."""
        if not title:
            raise ValueError("Post must have a title.")

        if not any(phrase in title for phrase in self.CLICKBAIT_PHRASES):
            raise ValueError(
                "Post title must contain 'Won't Believe', 'Secret', 'Top', or 'Guess'."
            )

        return title

    @validates('content')
    def validate_content(self, key, content):
        """Require post content of at least 250 characters."""
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        """Allow a missing summary, but cap any provided summary at 250 characters."""
        if summary is not None and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        """Allow only the editorial categories Fiction and Non-Fiction."""
        if category not in self.ALLOWED_CATEGORIES:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
