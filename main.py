from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
#bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_library.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=True, nullable=False)
    rating= db.Column(db.String(120), unique=True, nullable=False)

class BookForm(FlaskForm):
    book = StringField('Book name', validators=[DataRequired()])
    author = StringField("Book author", validators=[DataRequired()])
    rating = SelectField("Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪","💪💪💪💪💪💪","💪💪💪💪💪💪💪","💪💪💪💪💪💪💪💪","💪💪💪💪💪💪💪💪💪"], validators=[DataRequired()])
    submit = SubmitField('Add Book')

db.create_all()
all_books = Book.query.all()


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(book=form.book.data, author=form.author.data, rating=form.rating.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

