from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://Jon:onegod@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

item_bid_table = Table("item_bid_association", Base.metadata,
                       Column("item_id", Integer, ForeignKey("items.id")),
                       Column("bid_id", Integer, ForeignKey("bids.id"))
                       )

class Item(Base):
    __tablename__= "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    bids = relationship("Bid", secondary="item_bid_association", backref="items")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items = relationship("Item", backref="users")
    bids = relationship("Bid", backref="users")


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

Base.metadata.create_all(engine)

joe = User(username="Joe", password="yeah123")
jane = User(username="Jane", password="nah456")
smiddie = User(username="Smiddie", password="giants789")
baseball = Item(name="Baseball", description="Rare Babe Ruth signed ball from early 20th Century")

joe_bid = Bid(price=500.75, user_id=joe.id)
jane_bid = Bid(price=625.25, user_id=jane.id)

smiddie.items = [baseball]
joe.bids = [joe_bid]
jane.bids = [jane_bid]
baseball.bids = [joe_bid, jane_bid]

session.add_all([joe, jane, smiddie, baseball, joe_bid, jane_bid])
session.commit()

print(baseball.name, baseball.description)

for bid in baseball.bids:
    print (bid.price, bid.users.username)
