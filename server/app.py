#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    result = []
    for bakery in bakeries:
        result.append({
            'id': bakery.id,
            'name': bakery.name,
            'baked_goods': [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in bakery.baked_goods]
        })
    return jsonify(result)

    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        abort(404)
    result = {
        'id': bakery.id,
        'name': bakery.name,
        'baked_goods': [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in bakery.baked_goods]
    }
    return jsonify(result)


    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    result = [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in baked_goods]
    return jsonify(result)


    



@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not baked_good:
        abort(404)
    result = {
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
