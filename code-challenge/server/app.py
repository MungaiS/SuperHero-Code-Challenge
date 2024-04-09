from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = [hero.to_dict() for hero in Hero.query.all()]
    return jsonify(heroes), 200

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict_with_powers()), 200

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [power.to_dict() for power in powers]
    return jsonify(powers_data), 200

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict()), 200

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    data = request.json
    new_description = data.get('description')
    if new_description is not None and len(new_description) < 20:
        return jsonify({'error': 'Description must be at least 20 characters long'}), 400
    if new_description is not None:
        power.description = new_description
    db.session.commit()
    return jsonify(power.to_dict()), 200

@app.route('/hero_powers', methods=['POST'])
def add_hero_power():
    data = request.json
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')
    if None in (hero_id, power_id, strength):
        return jsonify({'error': 'Missing field(s)'}), 400
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not all((hero, power)):
        return jsonify({'error': 'Invalid hero or power id'}), 404
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'error': 'Invalid strength'}), 400
    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify({
        'id': hero_power.id,
        'hero_id': hero_power.hero_id,
        'power_id': hero_power.power_id,
        'strength': hero_power.strength
    }), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    