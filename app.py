from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertisements.db'
db = SQLAlchemy(app)

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    owner = db.Column(db.String(100), nullable=False)

@app.route('/advertisement', methods=['POST'])
def create_advertisement():
    data = request.get_json()
    new_advertisement = Advertisement(
        title=data['title'],
        description=data['description'],
        owner=data['owner']
    )
    db.session.add(new_advertisement)
    db.session.commit()
    return jsonify({'message': 'Объявление успешно создано'})

@app.route('/advertisement/<int:advertisement_id>', methods=['GET'])
def get_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement:
        return jsonify({
            'id': advertisement.id,
            'title': advertisement.title,
            'description': advertisement.description,
            'created_date': advertisement.created_date,
            'owner': advertisement.owner
        })
    else:
        return jsonify({'message': 'Объявление не найдено'})

@app.route('/advertisement/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if advertisement:
        db.session.delete(advertisement)
        db.session.commit()
        return jsonify({'message': 'Объявление успешно удалено'})
    else:
        return jsonify({'message': 'Объявление не найдено'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()