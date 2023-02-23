import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher{self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f'Book {self.id}: {self.title}'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.String(length=40), nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:Wordpass2019.@localhost:5432/mro"


engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


publisher1 = Publisher(id=1, name="Hamingway")


#session.add(publisher1)
#session.commit()


bk1 = Book(id=1, title='A Farewell to Arms', publisher_id=1)
bk2 = Book(id=2, title='For Whom the Bell Tolls', publisher_id=1)
bk3 = Book(id=3, title='The Old Man and the Sea', publisher_id=1)
bk4 = Book(id=4, title='The Sun Also Rises', publisher_id=1)
bk5 = Book(id=5, title='Death in the Afternoon', publisher_id=1)


#session.add_all([bk1, bk2, bk3, bk4, bk5])
#session.commit()


shp1 = Shop(id=1, name='Labirint')
shp2 = Shop(id=2, name='Bookvoed')
shp3 = Shop(id=3, name='Ozon')


#session.add_all([shp1, shp2, shp3])
#session.commit()


st1 = Stock(id=1, book_id=1, shop_id=3, count=1)
st2 = Stock(id=2, book_id=2, shop_id=2, count=2)
st3 = Stock(id=3, book_id=3, shop_id=2, count=3)
st4 = Stock(id=4, book_id=4, shop_id=1, count=4)
st5 = Stock(id=5, book_id=5, shop_id=3, count=5)

#session.add_all([st1, st2, st3, st4, st5])
#session.commit()

sl1 = Sale(id=1, price=600, date_sale='09-11-2022', stock_id=1, count=1)
sl2 = Sale(id=2, price=500, date_sale='08-11-2022', stock_id=2, count=2)
sl3 = Sale(id=3, price=580, date_sale='05-11-2022', stock_id=3, count=3)
sl4 = Sale(id=4, price=490, date_sale='02-11-2022', stock_id=4, count=4)
sl5 = Sale(id=5, price=600, date_sale='26-10-2022', stock_id=5, count=5)

#session.add_all([sl1, sl2, sl3, sl4, sl5])
#session.commit()

query = session.query(Stock, Book.title, Shop.name, Sale.price, Sale.date_sale)
query = query.join(Sale)
query = query.join(Shop)
query = query.join(Book)
query = query.join(Publisher)
for c in query.filter(Publisher.name == input('Enter the name of publisher: ')):
    print(c[1:])

session.close()


