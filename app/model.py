from app import db
from random import seed
from app.util import hash_password
import forgery_py
import random
import time

class Melon(db.Model):
    __tablename__ = 'melons'
    
    id          = db.Column(db.Integer, primary_key=True)
    melon_type  = db.Column(db.String(30))
    common_name = db.Column(db.String(30))
    price       = db.Column(db.Numeric(8, 2))
    imgurl      = db.Column(db.String(200))



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
    def generate_fake():
        seed()

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
        if random.random() < .24:
            c.shipto_address1   = forgery_py.address.street_address()
            c.shipto_city       = forgery_py.address.city()
            c.shipto_state      = forgery_py.address.state_abbrev()
            c.shipto_postalcode = forgery_py.address.zip_code()
        else:
            c.shipto_address1   = c.billto_address1
            c.shipto_city       = c.billto_city
            c.shipto_state      = c.billto_state
            c.shipto_postalcode = c.billto_postalcode
        
        return c


class Order(db.Model):
    __tablename__ = 'orders'

    status_list = ['New', 'Processing', 'Out for Delivery', 'Delivered', 'Canceled']
    delivery_method_list = ['UberMelon', 'UberMelonX', 'UberFresh']

    id                 = db.Column(db.Integer, primary_key=True)
    customer_id        = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, index=True)

    status             = db.Column(db.Enum('New', 'Processing', 'Out for Delivery', 'Delivered', 'Canceled'))
    created_at         = db.Column(db.Integer, nullable=False) # epoch datetime
    salesperson_id     = db.Column(db.Integer, db.ForeignKey('salespeople.id'), nullable=True, index=True)

    shipto_address1    = db.Column(db.String(40))
    shipto_address2    = db.Column(db.String(40))
    shipto_city        = db.Column(db.String(35))
    shipto_state       = db.Column(db.String(35))
    shipto_postalcode  = db.Column(db.String(10))

    subtotal           = db.Column(db.Numeric(10, 2))
    tax                = db.Column(db.Numeric(10, 2))
    delivery_method    = db.Column(db.String(20))
    delivery_amount    = db.Column(db.Numeric(10, 2))
    order_total        = db.Column(db.Numeric(10, 2))
    
    customer    = db.relationship('Customer', backref='orders')
    salesperson = db.relationship('SalesPerson', backref='orders')


    # Generate a fake record
    @staticmethod
    def generate_fake():
        seed()

        o = Order()
        o.status = random.choice(o.status_list)
        o.created_at = int(time.time()) - (60*60*24) * (random.random() * 100)

        # Get a random customer record
        c = None
        count = 0
        while not c and count < 100:
            c = Customer.query.offset(random.randint(0, Customer.query.count())).first()
            count += 1
        o.customer = c

        # There's a 60% chance a salesperson assisted with this order
        if random.random() < .60:
            s = SalesPerson.query.offset(random.randint(0, SalesPerson.query.count())).first()
            o.salesperson = s

        # There's a 15% chance the customer shipped to a different address
        if random.random() < .15:
            o.shipto_address1   = forgery_py.address.street_address()
            o.shipto_city       = forgery_py.address.city()
            o.shipto_state      = forgery_py.address.state_abbrev()
            o.shipto_postalcode = forgery_py.address.zip_code()
        else:
            o.shipto_address1   = c.shipto_address1
            o.shipto_address2   = c.shipto_address2
            o.city              = c.shipto_city
            o.state             = c.shipto_state
            o.postalcode        = c.shipto_postalcode

        o.delivery_method = random.choice(o.delivery_method_list)
        o.delivery_amount = int ( (random.random() * 1800) + 200 ) / 100.0
        o.subtotal    = 0.0
        o.tax         = 0.0
        o.order_total = 0.0
        return o






class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id            = db.Column(db.Integer, primary_key=True)
    order_id      = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    melon_id      = db.Column(db.Integer, db.ForeignKey('melons.id'), nullable=False, index=True)
    quantity      = db.Column(db.Integer, default=1)
    unit_price    = db.Column(db.Numeric(8, 2))
    total_price   = db.Column(db.Numeric(10, 2))
    
    order    = db.relationship('Order', backref='items')
    melon    = db.relationship('Melon', backref='orderitems')


    # Generate a fake record
    @staticmethod
    def generate_fake():
        seed()

        i = OrderItem()

        m = None
        while not m:
            m = Melon.query.offset(random.randint(0, Melon.query.count())).first()
        i.melon = m
        # 20% chance this might be a large order
        if random.random() < .20:
            i.quantity = int(random.random() * 100)
        else:
            i.quantity = int(random.random() * 10) + 1

        i.unit_price  = m.price
        i.total_price = float(i.unit_price) * float(i.quantity)

        return i



REGIONS_LIST = ['Northeast', 'Northwest', 'Southeast', 'Southwest', 'Central']
class SalesPerson(db.Model):
    __tablename__ = 'salespeople'

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password      = db.Column(db.String(200))     # hash
    givenname     = db.Column(db.String(30))
    surname       = db.Column(db.String(30))
    telephone     = db.Column(db.String(20))

    region        = db.Column(db.String(20))


    # Generate a fake record
    @staticmethod
    def generate_fake():
        seed()

        sp = SalesPerson(
                email           = forgery_py.internet.email_address(),
                password        = hash_password(forgery_py.lorem_ipsum.word()),
                givenname       = forgery_py.name.first_name(),
                surname         = forgery_py.name.last_name(),
                telephone       = forgery_py.address.phone(),
                region          = random.choice(REGIONS_LIST)
            )

        return sp
