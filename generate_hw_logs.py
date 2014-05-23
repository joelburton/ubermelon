#
# generates sample log files for homeworks
#

import json
import datetime
import os
from app.model import *
from app import db

HOMEWORK_DIR='homework'


def dircheck(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


# Generate log file for the last week of deliveries
def homework01_log():
    hwpath = HOMEWORK_DIR + '/hw01'
    dircheck(hwpath)

    # Get the max order data
    (maxdate,) = db.session.query(db.func.max(Order.created_at)).first()
    # Subtract a week
    maxdate -= 60*60*24*7

    orders = Order.query.filter_by(status='Delivered').filter(Order.delivered_at > maxdate).order_by('delivered_at').all()

    f = open(hwpath + '/um-server-01.log', 'w')

    for order in orders:
        delivered = datetime.datetime.fromtimestamp(order.delivered_at)

        for item in order.items:
            f.write( "%s: %d %s delivered to User %d" % (
                        delivered.strftime('%a %Y-%m-%d'),
                        item.quantity, 
                        item.melon.common_name, 
                        order.customer_id
                ) )
            f.write("\n")

    f.close()


# Generate 3 log files with melon counts and order totals for a given day
def homework02_log():
    hwpath = HOMEWORK_DIR + '/hw02'
    dircheck(hwpath)
    
    # Get the max order data
    (maxepoch,) = db.session.query(db.func.max(Order.created_at)).first()
    maxdate = datetime.date.fromtimestamp(maxepoch)

    for i in range(1, 4):
        maxdate -= datetime.timedelta(days=1)
        datestamp = maxdate.strftime('%Y%m%d')
        
        # Get the epoch range for the day
        endrange = int(maxdate.strftime('%s'))
        startrange = endrange - 60*60*24
        
        # Get the orders in the date range
        orders = Order.query.filter_by(status='Delivered').filter(Order.delivered_at > startrange).filter(Order.delivered_at < endrange).order_by('delivered_at').all()
        
        melons = {}
        for order in orders:
            for item in order.items:
                melons.setdefault(item.melon.common_name, {})
                melons[item.melon.common_name]['count'] = melons[item.melon.common_name].get('count', 0) + item.quantity
                melons[item.melon.common_name]['amount'] = melons[item.melon.common_name].get('amount', 0.0) + (item.quantity * float(item.unit_price))
        
        
        f = open(hwpath + '/um-deliveries-%s.csv' % datestamp, 'w')
        for melon in sorted(melons.keys()):
            f.write(','.join([melon, 
                              str(melons[melon].get('count', 0)),
                              str(melons[melon].get('amount', 0))
                              ]))
            f.write("\n")
        f.close()

# Generate 3 log files, one for each week of deliveries
def homework02_log_old():
    hwpath = HOMEWORK_DIR + '/hw02'
    dircheck(hwpath)

    # Get the max order data
    (maxepoch,) = db.session.query(db.func.max(Order.created_at)).first()
    maxdate = datetime.date.fromtimestamp(maxepoch)
    # Subtract 1 day
    maxdate -= datetime.timedelta(days=1)
    
    # Repeat
    for i in range(1, 4):
        # Go back a week
        endrange = maxdate.strftime('%s')
        datestamp = maxdate.strftime('%Y%m%d')
        maxdate -= datetime.timedelta(days=7)
        startrange = maxdate.strftime('%s')

        # Get the orders in the date range
        orders = Order.query.filter_by(status='Delivered').filter(Order.delivered_at > startrange).filter(Order.delivered_at < endrange).order_by('delivered_at').all()

        f = open(hwpath + '/um-deliveries-%s.csv' % datestamp, 'w')
        f.write('date,customer_id,city,state,melons_delivered,total_amount\n')
    
        for order in orders:
            delivered = datetime.datetime.fromtimestamp(order.delivered_at)
    
            num_melons = 0
            for item in order.items:
                num_melons += item.quantity

            f.write(','.join([
                delivered.strftime('%Y-%m-%d'),
                str(order.customer_id),
                order.shipto_city,
                order.shipto_state,
                str(num_melons),
                str(order.order_total)
            ]))
            f.write("\n")

        f.close()
    

# melon data dictionary definitions
def homework06_py():
    hwpath = HOMEWORK_DIR + '/hw06'
    dircheck(hwpath)
    
    melons_py = hwpath + '/melons.py'
    
    # Load the Melons
    melondata = Melon.query.limit(5).all()
    
    melons = {}
    for melon in melondata:
        m = {
            'name': melon.common_name,
            'seedless': melon.seedless,
            'price': melon.price
        }
        melons[melon.id] = m
    
    f = open(melons_py, 'w')
    
    f.write('melon_name = {\n')
    for key in melons.keys():
        f.write('    %s: "%s",\n' % (key, melons[key]['name']))
    f.write("}\n\n")

    f.write('melon_price = {\n')
    for key in melons.keys():
        f.write('    %s: %s,\n' % (key, melons[key]['price']))
    f.write("}\n\n")

    f.write('melon_seedless = {\n')
    for key in melons.keys():
        f.write('    %s: %s,\n' % (key, melons[key]['seedless']))
    f.write("}\n\n")
    
    f.close()


# csv files for SQL Homework
def homework07_csv():
    hwpath = HOMEWORK_DIR + '/hw07'
    dircheck(hwpath)

    customers_csv = hwpath + '/customers.csv'
    orders_csv = hwpath + '/orders.csv'

    # Generate customers.csv
    customers = Customer.query.order_by('id').all()
    
    random.seed()
    f = open(customers_csv, 'w')
    f.write('customer_id,first,last,email,telephone,called\n')
    for customer in customers:
        # 10% chance we've called the customer
        calleddate = ""
        if random.random() < .15:
            calleddate = (datetime.datetime.now() - datetime.timedelta(days=int(random.randint(1, 60)))).strftime('%m/%d/%Y')

        f.write(','.join([str(customer.id), customer.givenname, customer.surname, 
                          customer.email, customer.telephone, calleddate]))
        f.write("\n")

    f.close()

    # Generate orders.csv
    orders = Order.query.filter(Order.created_at > (time.time() - 60*60*24*30)).all()

    f = open(orders_csv, 'w')
    f.write('order_id,order_date,status,customer_id,email,address,city,state,postalcode,num_watermelons,num_othermelons,subtotal,tax,order_total\n')

    for order in orders:
        wmcount = 0
        othercount = 0

        for item in order.items:
            if item.melon.melon_type == 'Watermelon':
                wmcount += item.quantity
            else:
                othercount += item.quantity

        f.write(','.join([
                str(order.id),
                datetime.datetime.fromtimestamp(order.created_at).strftime('%m/%d/%Y'),
                order.status,
                str(order.customer_id),
                order.customer.email,
                order.shipto_address1,
                order.shipto_city,
                order.shipto_state,
                order.shipto_postalcode,
                str(wmcount),
                str(othercount),
                str(order.subtotal),
                str(order.tax),
                str(order.order_total)
            ]).encode('utf8'))
        f.write("\n")

def generate_logs():
    print "Generating:"
    print "Homework 01"
    homework01_log()
    print "Homework 02"
    homework02_log()
    print "Homework 06"
    homework06_py()
    print "Homework 07"
    homework07_csv()
    pass


def main():
    generate_logs()


if __name__ == '__main__':
    main()