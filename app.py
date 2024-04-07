from flask import Flask, render_template, url_for, redirect, request  
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from forms import BookForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)


class Book(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       author = db.Column(db.String(100), nullable=False)
       title = db.Column(db.String(100), nullable=False)
       genre = db.Column(db.String(50), nullable=False)
       date_received = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
       price = db.Column(db.Float, nullable=False)  # Поле цены как десятичное число


@app.route('/', methods=['POST', 'GET'])
def index():
    form = BookForm()

    if form.validate_on_submit():
        author = form.author.data
        title = form.title.data
        genre = form.genre.data
        date_received = form.date_received.data
        price = form.price.data

        book = Book(author=author, title=title, 
                          genre=genre, date_received=date_received, price=price)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

    books = Book.query.all()
    return render_template('index.html', form=form, books=books)


@app.route('/books/<int:id>')
def book_detail(id):
    book = Book.query.get(id)   
    return render_template("book_detail.html", book=book)

@app.route('/books/<int:id>/update', methods=['POST', 'GET'])
def book_update(id):    
    book = Book.query.get(id)
    form = BookForm(obj=book)
    if request.method == 'POST':
        book.author = request.form['author']
        book.title = request.form['title']
        book.genre = request.form['genre']
        book.date_received = datetime.strptime(request.form['date_received'], '%Y-%m-%d')
        book.price = request.form['price']
        try:            
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
           return f"При изменении книги произошла ошибка: {str(e)}"
    else:
        
        return render_template("book_update.html", book=book, form=form)
    

@app.route('/books/<int:id>/delete')
def book_delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "При удалении книги произошла ошибка!!!"
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
