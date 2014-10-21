from flask import Flask, request, render_template, Response
from app import app, db
from app.model import *

import json


@app.route("/")
def index():
	return "hello"

@app.route("/melons")
def melons_list():
	melons = Melon.query.all()
	resp = { 'melons': [] }

	for melon in melons:
		price = melon.price
		try:
			price = float(melon.price)
		except:
			pass

		resp['melons'].append({ 'common_name': melon.common_name,
					  'melon_id': melon.id,
					  'melon_type': melon.melon_type,
					  'price': price })

	resp['count'] = len(resp['melons'])

	return Response(json.dumps(resp), mimetype='application/json')

@app.route("/melon/<int:melon_id>")
def melon_info(melon_id):
	resp = {}

	melon = Melon.query.get(melon_id)

	if melon:
		resp['id'] = melon.id
		resp['melon_type'] = melon.melon_type
		resp['common_name'] = melon.common_name
		resp['price'] = float(melon.price)
		resp['seedless'] = melon.seedless
		resp['imgurl'] = melon.imgurl

	return Response(json.dumps(resp), mimetype='application/json')
