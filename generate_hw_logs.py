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


def homework01_log():
	hwpath = HOMEWORK_DIR + '/hw01'
	dircheck(hwpath)

	orders = Order.query.filter_by(status='Delivered').order_by('delivered_at').all()

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
	homework01_log()
	homework07_csv()
	pass


def main():
	generate_logs()


if __name__ == '__main__':
	main()