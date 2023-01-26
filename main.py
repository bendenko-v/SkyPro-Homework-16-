import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from utils import get_user, get_order, get_offer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False

db = SQLAlchemy(app)


class User(db.Model):
    """ Модель пользователя"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(100))
    last_name = db.Column(db.Text(100))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(100))
    role = db.Column(db.Text(10))
    phone = db.Column(db.Text(20))


class Order(db.Model):
    """ Модель заказа"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(200))
    description = db.Column(db.Text(500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.Text(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    """ Модель предложения """
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def check_customer(data: dict, role: str) -> bool:
    """ Проверка является ли пользователь исполнителем"""
    user_customer = db.session.query(User).get(data[role])
    if user_customer.role == 'customer':
        return True
    return False


@app.get('/users')
def users():
    all_users = db.session.query(User)
    result = []
    for user in all_users:
        result.append(get_user(user))
    return result


@app.get('/users/<int:uid>')
def user_by_id(uid):
    user = db.session.query(User).get(uid)
    if user:
        return get_user(user)
    return f'Нет пользователя с id {uid}!'


@app.post('/users')
def add_user():
    if request.json:
        data = request.json
    else:
        return 'Не получилось добавить пользователя!'

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        email=data['email'],
        role=data['role'],
        phone=data['phone']
    )
    db.session.add(new_user)
    db.session.commit()
    return f'Пользователь {new_user} добавлен в таблицу Users!'


@app.put('/users/<int:uid>')
def update_user_by_id(uid):
    if request.json:
        data = request.json
    else:
        return f'Не получилось обновить данные пользователя c id {uid}!'
    user = db.session.query(User).get(uid)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.age = data['age']
    user.email = data['email']
    user.role = data['role']
    user.phone = data['phone']
    db.session.add(user)
    db.session.commit()
    return f'Данные пользователя {user} были обновлены!'


@app.delete('/users/<int:uid>')
def delete_user_by_id(uid):
    user = db.session.query(User).get(uid)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'Данные пользователя c id {uid} были удалены!'
    return f'Нет пользователя с id {uid}! Удаление невозможно!'


@app.get('/orders')
def orders():
    all_orders = db.session.query(Order)
    result = []
    for order in all_orders:
        result.append(get_order(order))
    return result


@app.get('/orders/<int:uid>')
def order_by_id(uid):
    order = db.session.query(Order).get(uid)
    if order:
        return get_order(order)
    return f'Нет заказа с id {uid}!'


@app.post('/orders')
def add_order():
    if request.json:
        data = request.json
    else:
        return 'Не получилось добавить заказ!'

    if not check_customer(data, 'customer_id'):
        return f"Пользователь {data['customer_id']} не является заказчиком! Нельзя создать для него заказ!"

    if check_customer(data, 'executor_id'):
        return f"Пользователь {data['executor_id']} не является исполнителем! Нельзя создать для него заказ!"

    month_start, day_start, year_start = data['start_date'].split('/')
    month_end, day_end, year_end = data['end_date'].split('/')

    new_order = Order(
        name=data['name'],
        description=data['description'],
        start_date=datetime.date(int(year_start), int(month_start), int(day_start)),
        end_date=datetime.date(int(year_end), int(month_end), int(day_end)),
        address=data['address'],
        price=data['price'],
        customer_id=data['customer_id'],
        executor_id=data['executor_id']
    )
    db.session.add(new_order)
    db.session.commit()
    return f'Заказ {new_order} добавлен в таблицу Orders!'


@app.put('/orders/<int:uid>')
def update_order_by_id(uid):
    if request.json:
        data = request.json
    else:
        return f'Не получилось обновить данные заказа c id {uid}!'
    order = db.session.query(Order).get(uid)

    if not check_customer(data, 'customer_id'):
        return f"Пользователь {data['customer_id']} не является заказчиком! Нельзя внести изменения в заказ!"

    if check_customer(data, 'executor_id'):
        return f"Пользователь {data['executor_id']} не является исполнителем! Нельзя внести изменения в заказ!"

    month_start, day_start, year_start = data['start_date'].split('/')
    month_end, day_end, year_end = data['end_date'].split('/')

    order.name = data['name']
    order.description = data['description']
    order.start_date = datetime.date(int(year_start), int(month_start), int(day_start))
    order.end_date = datetime.date(int(year_end), int(month_end), int(day_end))
    order.address = data['address']
    order.price = data['price']
    order.customer_id = data['customer_id']
    order.executor_id = data['executor_id']
    db.session.add(order)
    db.session.commit()
    return f'Данные заказа {order} были обновлены!'


@app.delete('/orders/<int:uid>')
def delete_order_by_id(uid):
    order = db.session.query(Order).get(uid)
    if order:
        db.session.delete(order)
        db.session.commit()
        return f'Данные заказа c id {uid} были удалены!'
    return f'Нет заказа с id {uid}! Удаление невозможно!'


@app.get('/offers')
def offers():
    all_offers = db.session.query(Offer)
    result = []
    for offer in all_offers:
        result.append(get_offer(offer))
    return result


@app.get('/offers/<int:uid>')
def offer_by_id(uid):
    offer = db.session.query(Offer).get(uid)
    if offer:
        return get_offer(offer)
    return f'Нет предложения с id {uid}!'


@app.post('/offers')
def add_offer():
    if request.json:
        data = request.json
    else:
        return 'Не получилось добавить предложение!'

    if check_customer(data, 'executor_id'):
        return f"Пользователь {data['executor_id']} не является исполнителем! Нельзя назначить предложение для него!"

    new_offer = Offer(
        order_id=data['order_id'],
        executor_id=data['executor_id']
    )
    db.session.add(new_offer)
    db.session.commit()
    return f'Предложение {new_offer} добавлено в таблицу Offers!'


@app.put('/offers/<int:uid>')
def update_offer_by_id(uid):
    if request.json:
        data = request.json
    else:
        return f'Не получилось обновить данные предложения c id {uid}!'

    if check_customer(data, 'executor_id'):
        return f"Пользователь {data['executor_id']} не является исполнителем! " \
               f"Нельзя внести изменения и назначить его исполнителем!"

    offer = db.session.query(Offer).get(uid)
    offer.order_id = data['order_id']
    offer.executor_id = data['executor_id']
    db.session.add(offer)
    db.session.commit()
    return f'Данные предложения {offer} были обновлены!'


@app.delete('/offers/<int:uid>')
def delete_offer_by_id(uid):
    offer = db.session.query(Offer).get(uid)
    if offer:
        db.session.delete(offer)
        db.session.commit()
        return f'Данные предложения c id {uid} были удалены!'
    return f'Нет предложения с id {uid}! Удаление невозможно!'


if __name__ == '__main__':
    app.run(debug=True)
