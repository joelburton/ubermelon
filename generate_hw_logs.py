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

def generate_logs():
	homework01_log()
	pass


def main():
	generate_logs()


if __name__ == '__main__':
	main()