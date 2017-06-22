from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Cloth, Base, Item, Vidit

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
brand = Cloth(user_id=1, name="Adidas")

session.add(brand)
session.commit()

item_1 = Item(user_id=1, name="One Piece", description="Western dress for women",
                     price="$7.50", course="Entree", restaurant=brand)

session.add(item_1)
session.commit()


item_2 = Item(user_id=1, name="Suit", description="Professional Cloths for men",
                     price="Rs.300", course="Appetizer", restaurant=brand)

session.add(item_2)
session.commit()

item_3 = Item(user_id=1, name="Dhoti", description="Fmaous eastren India dress",
                     price="Rs.550", course="Entree", restaurant=brand)

session.add(item_3)
session.commit()


# Menu for Super Stir Fry
brand1 = Cloth(user_id=1, name="Reebok")

session.add(brand1)
session.commit()


menuItem1 = Item(user_id=1, name="Lungi", description="One of the most traditional indian dress",
                     price="Rs.100", course="Entree", restaurant=brand1)

session.add(menuItem1)
session.commit()

menuItem2 = Item(user_id=1, name="saree",
                     description="Famous indian dress for women", price="Rs.250", course="Entree", restaurant=brand1)

session.add(menuItem2)
session.commit()


# Menu for Panda Garden
brand2 = Cloth(user_id=1, name="Puma")

session.add(brand2)
session.commit()


menuItem1 = Item(user_id=1, name="Jeans Shirt", description="Regular cloths for people",
                     price="Rs.800", course="Entree", restaurant=brand2)

session.add(menuItem1)
session.commit()


menuItem4 = Item(user_id=1, name="salwar kameej", description="North indian dress for women",
                     price="Rs.1000", course="Appetizer", restaurant=brand2)

session.add(menuItem4)
session.commit()

menuItem2 = Item(user_id=1, name="One Piece", description="Western dress for girls",
                     price="Rs900", course="Entree", restaurant=brand2)

session.add(menuItem2)
session.commit()


# Menu for Thyme for that
brand3 = Cloth(user_id=1, name="Levi's")

session.add(brand3)
session.commit()


menuItem1 = Item(user_id=1, name="Shirt", description="Formal wear",
                     price="Rs.500", course="Entree", restaurant=brand3)

session.add(menuItem1)
session.commit()


menuItem3 = Item(user_id=1, name="Track suit",
                     description="Cloths for jogging , running etc.", price="Rs.1000", course="Appetizer", restaurant=brand3)

session.add(menuItem3)
session.commit()

menuItem4 = Item(user_id=1, name="Gown", description="Long dress for ladies",
                     price="Rs.1500", course="Appetizer", restaurant=brand3)

session.add(menuItem4)
session.commit()



# Menu for Tony's Bistro
brand4 = Cloth(user_id=1, name="Nike")

session.add(brand4)
session.commit()


menuItem1 = Item(user_id=1, name="Swim Suit", description="Cloths for swimming",
                     price="Rs.1000", course="Appetizer", restaurant=brand4)

session.add(menuItem1)
session.commit()

menuItem2 = Item(user_id=1, name="Aprin", description="Cloth for kitchen work",
                     price="Rs.400", course="Entree", restaurant=brand4)

session.add(menuItem2)
session.commit()

menuItem3 = Item(user_id=1, name="suit", description="indian traditional dress",
                     price="Rs.800", course="Entree", restaurant=brand4)

session.add(menuItem3)
session.commit()


print "new cloth brands added"