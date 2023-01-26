"""
Используется один раз для заполнения данных в базе данных
"""

import datetime

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
    month_start, day_start, year_start = order['start_date'].split('/')
    month_end, day_end, year_end = order['end_date'].split('/')
    orders.append(
        Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(int(year_start), int(month_start), int(day_start)),
            end_date=datetime.date(int(year_end), int(month_end), int(day_end)),
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
