#
# generates sample data
#

import json
from app.model import *
from app import db

# Erases all data in the database!  Wheee
def erase_data():
	db.session.execute('DELETE FROM order_items')
	db.session.execute('DELETE FROM orders')
	db.session.execute('DELETE FROM customers')
	db.session.execute('DELETE FROM salespeople')
	db.session.execute('DELETE FROM melons')


def generate_melons():
	f = open('seed/melons.json')
	melons_json = f.read()
	melons = json.loads(melons_json)

	for melon in melons:
		m = Melon()
		m.melon_type  = melon['type']
		m.common_name = melon['name']
		m.price       = melon['price']
		m.imgurl      = melon['imgurl']

		db.session.add(m)

	db.session.commit()


def generate_salespeople():
	for i in range(250):
		sp = SalesPerson.generate_fake()

		db.session.add(sp)

	db.session.commit()


# Creates 1000 customer records
def generate_customers():
	emails = {}

	while len(emails.keys()) < 1000:
		c = Customer.generate_fake()
		if c.email not in emails.keys():
			emails[c.email] = 1
			db.session.add(c)

	db.session.commit()

def generate_orders():
	target = 10000

	for i in range(target):
		o = Order.generate_fake()

		# Generate items for this order
		for x in range(int(random.random() * 5) + 1):
			item = OrderItem.generate_fake()
			o.items.append(item)
			o.subtotal += item.total_price

		# Calculate tax and total
		o.tax = o.subtotal * 0.06
		o.order_total = o.subtotal + o.delivery_amount + o.tax

		db.session.add(o)

		if ((i+1) % 100) == 0:
			db.session.commit()
			print "Generated %d/%d Orders" % (Order.query.count(), target)

	db.session.commit()


def main():
	erase_data()

	generate_melons()
	print "Generated %d Melons" % (Melon.query.count())
	generate_salespeople()
	print "Generated %d Sales People" % (SalesPerson.query.count())
	generate_customers()
	print "Generated %d Customers" % (Customer.query.count())
	generate_orders()
	print "Generated %d Orders" % (Order.query.count())


if __name__ == '__main__':
	main()