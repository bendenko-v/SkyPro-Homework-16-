def get_user(user: object) -> dict:
    """
    Get SQLAlchemy db.Model object User() and serialize it to Python dictionary
    Args:
        user: class User() object

    Returns:
        dict with user data
    """
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'role': user.role,
        'phone': user.phone
    }


def get_order(order: object) -> dict:
    """
    Get SQLAlchemy db.Model object Order() and serialize it to Python dictionary
    Args:
        order: class Order() object

    Returns:
        dict with order data
    """
    return {
        'id': order.id,
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price,
        'customer_id': order.customer_id,
        'executor_id': order.executor_id
    }


def get_offer(offer: object) -> dict:
    """
    Get SQLAlchemy db.Model object Offer() and serialize it to Python dictionary
    Args:
        offer: class Offer() object

    Returns:
        dict with offer data
    """
    return {
        'id': offer.id,
        'order_id': offer.order_id,
        'executor_id': offer.executor_id
    }
