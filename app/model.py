from app import db
from random import seed
from app.util import hash_password
import forgery_py
import random

class Melon(db.Model):
    __tablename__ = 'melons'
    
    id          = db.Column(db.Integer, primary_key=True)
    melon_type  = db.Column(db.String(30))
    common_name = db.Column(db.String(30))


class Customer(db.Model):
    __tablename__ = 'customers'

    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(120), index=True, unique=True, nullable=False)
    givenname   = db.Column(db.String(30))
    surname     = db.Column(db.String(30))
    password    = db.Column(db.String(200))     # hash
    telephone   = db.Column(db.String(20))
    tos_agree   = db.Column(db.Integer)         # epoch datetime
    gender      = db.Column(db.Enum('Not Specified', 'Male', 'Female', 'Other'))
    dob         = db.Column(db.Date())

    billto_address1    = db.Column(db.String(40))
    billto_address2    = db.Column(db.String(40))
    billto_city        = db.Column(db.String(35))
    billto_state       = db.Column(db.String(35))
    billto_postalcode  = db.Column(db.String(10))

    shipto_address1    = db.Column(db.String(40))
    shipto_address2    = db.Column(db.String(40))
    shipto_city        = db.Column(db.String(35))
    shipto_state       = db.Column(db.String(35))
    shipto_postalcode  = db.Column(db.String(10))

    region             = db.Column(db.String(20))


    # Generate a fake record
    @staticmethod
    def generate_fake(count=1):
        seed()

        for i in range(count):
            c = Customer(
                    givenname       = forgery_py.name.first_name(),
                    surname         = forgery_py.name.last_name(),
                    email           = forgery_py.internet.email_address(),
                    password        = hash_password(forgery_py.lorem_ipsum.word()),
                    dob             = forgery_py.date.date(True),
                    billto_address1 = forgery_py.address.street_address(),
                    billto_city       = forgery_py.address.city(),
                    billto_state      = forgery_py.address.state_abbrev(),
                    billto_postalcode = forgery_py.address.zip_code(),

                    telephone       = forgery_py.address.phone(),
                    gender          = forgery_py.personal.gender(),

                )
            
            # There's a 24% chance the billing and shipping address might differ
            if random.random < .24:
                c.shipto_address1 = forgery_py.address.street_address(),
                c.shipto_city       = forgery_py.address.city(),
                c.shipto_state      = forgery_py.address.state_abbrev(),
                c.shipto_postalcode = forgery_py.address.zip_code(),
            else:
                c.shipto_address1   = c.billto_address1
                c.shipto_city       = c.billto_city
                c.shipto_state      = c.billto_state
                c.shipto_postalcode = c.billto_postalcode
            
            return c


""""
class Order(db.Model):
    __tablename__ = 'orders'

    id
    customer_id
    ship_address
    ship_city
    ship_state
    ship_postalcode
    subtotal
    tax
    delivery
    totalamount



class OrderItems(db.Model):
    __tablename__ = 'order_items'


class Salespeople(db.Model):
    __tablename__ = 'salespeople'

    """
