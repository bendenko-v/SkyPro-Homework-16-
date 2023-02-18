"""
Используется один раз для заполнения данных в базе данных
"""

from datetime import datetime

from main import app, db, User, Order, Offer
from data import USERS, ORDERS, OFFERS

users = []
orders = []
offers = []

for user in USERS:
    users.append(
        User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone'],
        )
    )

for order in ORDERS:
    orders.append(
        Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
            end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
    )

for offer in OFFERS:
    offers.append(
        Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
    )

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    db.session.add_all(orders)
    db.session.commit()
    db.session.add_all(offers)
    db.session.commit()
