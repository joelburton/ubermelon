from app import db

class Melon(db.Model):
	__tablename__ = 'melons'

	id
	type
	common name


class Customer(db.Model):
	__tablename__ = 'customers'

	id
	email
	password
	first name
	last name
	billto_address
	billto_city
	billto_state
	billto_postalcode
	shipto_address
	shipto_city
	shipto_state
	shipto_postalcode
	region


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

	
