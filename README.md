# SkyPro / Homework 16

SQLAlchemy models for:
- users (can be customer or executor);
- orders (only a user with the customer role can create an order);
- offers (only a user with the executor role can respond to the order and create an offer).

## Usage

Run "main.py" to start the Flask app.

## App features

* The '/users' view returns a JSON with all users (customers and executors).
* The '/users/(id)' view returns a JSON with user by id.
* The '/orders' view returns a JSON with all orders.
* The '/orders/(id)' view returns a JSON with order by id.
* The '/offers' view returns a JSON with all offers.
* The '/offers/(id)' view returns a JSON with offer by id.

### Methods POST, PUT and DELETE working with all views:
* Use '/users' view with POST method and send JSON with user data;
* Use '/users/(id)' view with PUT and DELETE methods to change user data or delete user by id.
* Use '/orders' view with POST method and send JSON with order data;
* Use '/orders/(id)' view with PUT and DELETE methods to change order data or delete order by id.
* Use '/offers' view with POST method and send JSON with offer data;
* Use '/offers/(id)' view with PUT and DELETE methods to change offer data or delete offer by id.