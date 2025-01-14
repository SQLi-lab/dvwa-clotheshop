import json
import os
from urllib.parse import urlparse
from flask import Flask, Blueprint, request, jsonify, make_response
from flask_cors import CORS
from db import query_db, execute_db
import logging

# Инициализация Flask приложения
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["*"])

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для извлечения пути из переменной окружения
def extract_path_from_url(env_var_name, default='/lab/frontend/api'):
    full_url = os.getenv(env_var_name, default)
    logger.info(f"Full url {full_url}")
    if full_url == default:
        logger.info("No REACT_APP_BACKEND_URL env found, using defaults")
        return default
    parsed_url = urlparse(full_url)
    return parsed_url.path

url_prefix = extract_path_from_url('REACT_APP_BACKEND_URL')

# Создаем Blueprint
api = Blueprint('api', __name__, url_prefix=url_prefix)

# Роут для авторизации
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    query = f"SELECT * FROM users WHERE login = '{username}' AND password = '{password}'"
    user = query_db(query, one=True)

    if user:
        resp = make_response({"message": f"Login successful: user={user}"}, 200)
        cookie_value = f"user={username}; Path=/; SameSite=Lax"
        resp.headers.add('Set-Cookie', cookie_value)
        return resp
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Получение списка категорий
@api.route('/categories', methods=['GET'])
def get_categories():
    query = "SELECT DISTINCT category FROM product_categories"
    try:
        categories = query_db(query)
        result = [row['category'] for row in categories]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Роут для выхода
@api.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "Вы успешно вышли из системы"}))
    response.set_cookie('user', '', expires=0)
    logger.info("User logged out and cookie cleared")
    return response

# Получение списка продуктов
@api.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category', '')

    query = """
        SELECT 
            article, 
            name, 
            description, 
            category, 
            price, 
            stock, 
            released
        FROM products
        WHERE released = 1
    """
    if category:
        query += f" AND category = '{category}'"

    try:
        products = query_db(query)
        result = [dict(row) for row in products]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Получение информации о продукте
@api.route('/products/<int:article>', methods=['GET'])
def get_product(article):
    query = f"""
        SELECT 
            article, 
            name, 
            description, 
            category, 
            price, 
            stock, 
            released
        FROM products
        WHERE article = {article}
    """
    product = query_db(query, one=True)
    if product:
        return jsonify(dict(product))
    else:
        return jsonify({"message": "Product not found"}), 404

# Добавление отзыва о продукте
@api.route('/products/<int:article>/reviews', methods=['POST'])
def add_product_review(article):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]
    data = request.json
    review_text = data.get('review')
    rating = data.get('rating', 5)
    logger.info(rating)
    if not review_text or not rating:
        return jsonify({"error": "Review text and rating are required"}), 400

    query = f"""
        INSERT INTO reviews (article, login, review_text, review_date, rating)
        VALUES ({article}, '{username}', '{review_text}', datetime('now'), {rating})
    """

    try:
        execute_db(query)
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        logger.info(e)
        return jsonify({"error": str(e)}), 500

# Получение отзывов о продукте
@api.route('/products/<int:article>/reviews', methods=['GET', 'POST'])
def get_product_reviews(article):
    query = f"""
        SELECT 
            reviews.login, 
            reviews.review_text, 
            reviews.rating, 
            reviews.review_date
        FROM reviews
        WHERE reviews.article = {article}
    """
    try:
        reviews = query_db(query)
        reviews_list = [
            {
                "username": row["login"],
                "review_text": row["review_text"],
                "rating": row["rating"],
                "review_date": row["review_date"]
            }
            for row in reviews
        ]
        return jsonify(reviews_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Добавление товара в избранное
@api.route('/favorites', methods=['POST'])
def add_to_favorites():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]
    data = request.json
    article = data.get('article')

    logger.info(data)
    if not article:
        return jsonify({"message": "Invalid request data"}), 400
    logger.info(article)
    # Проверяем, существует ли уже такая запись
    check_query = f"""
        SELECT 1 FROM favorite_products WHERE login = '{username}' AND article = {article}
    """
    existing = query_db(check_query, one=True)
    logger.info(existing)

    if existing:
        logger.info("EXIST")

        return jsonify({"message": "Product is already in favorites"}), 400

    # Если записи нет, добавляем ее
    query = f"""
        INSERT INTO favorite_products (login, article, added_date, secret)
        VALUES ('{username}', {article}, datetime('now'), 'default_secret')
    """
    try:
        execute_db(query)
        return jsonify({"message": "Product added to favorites"}), 201
    except Exception as e:
        logger.info(e)
        return jsonify({"error": str(e)}), 500

# Получение отзывов пользователя
@api.route('/profile/reviews', methods=['GET'])
def user_reviews():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    query = f"""
        SELECT 
            reviews.review_text,
            reviews.rating,
            reviews.review_date,
            products.name AS product_name
        FROM reviews
        JOIN products ON reviews.article = products.article
        WHERE reviews.login = '{username}'
    """
    try:
        reviews = query_db(query)
        reviews_list = [
            {
                "review_text": row["review_text"],
                "rating": row["rating"],
                "review_date": row["review_date"],
                "product_name": row["product_name"]
            }
            for row in reviews
        ]
        return jsonify(reviews_list), 200
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        return jsonify({"error": str(e)}), 500

# Получение избранных машин пользователя
@api.route('/profile/favorites', methods=['GET'])
def user_favorites():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    query = f"""
        SELECT 
            products.name AS product_name,
            products.article,
            favorite_products.added_date
        FROM favorite_products
        JOIN products ON favorite_products.article = products.article
        WHERE favorite_products.login = '{username}'
    """
    try:
        favorites = query_db(query)
        favorites_list = [
            {
                "product_name": row["product_name"],
                "article": row["article"],
                "added_date": row["added_date"]
            }
            for row in favorites
        ]
        return jsonify({"favorites": favorites_list}), 200
    except Exception as e:
        logger.error(f"Error fetching favorites: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/favorites/check', methods=['POST'])
def check_favorite():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]
    data = request.json
    article = data.get("article")  # Используем `article` вместо `model_id`

    if not article:
        return jsonify({"message": "Article ID is required"}), 400

    # Проверяем, существует ли продукт в избранном
    query = f"SELECT 1 FROM favorite_products WHERE login = '{username}' AND article = {article}"
    try:
        result = query_db(query, one=True)
        return jsonify({"isFavorite": bool(result)})
    except Exception as e:
        logger.error(f"Error checking favorite: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/favorites/<int:article>', methods=['DELETE'])
def remove_from_favorites(article):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    # Удаление записи из базы данных
    query = f"DELETE FROM favorite_products WHERE login = '{username}' AND article = {article}"
    try:
        execute_db(query)
        return jsonify({"message": "Product removed from favorites"}), 200
    except Exception as e:
        logger.error(f"Error removing from favorites: {e}")
        return jsonify({"error": str(e)}), 500

# Получение информации профиля и обновление описания
@api.route('/profile', methods=['GET', 'POST'])
def profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    if request.method == 'GET':
        query_user = f"""
            SELECT 
                login, 
                name, 
                birth_date, 
                address, 
                phone_number
            FROM user_personal_info 
            WHERE login = '{username}'
        """
        user = query_db(query_user, one=True)

        if user:
            return jsonify({
                "username": user['login'],
                "name": user['name'],
                "birthDate": user['birth_date'],
                "address": user['address'],
                "phone": user['phone_number']
            })
        else:
            return jsonify({"message": "User not found"}), 404

    elif request.method == 'POST':
        data = request.json
        if not data or 'description' not in data:
            return jsonify({"message": "Invalid data"}), 400

        new_description = data['description']
        query = f"""
            UPDATE user_personal_info
            SET secret = '{new_description}'
            WHERE login = '{username}'
        """
        try:
            execute_db(query)
            return jsonify({"message": "Description updated successfully"}), 200
        except Exception as e:
            logger.error(f"Error updating description: {e}")
            return jsonify({"error": str(e)}), 500

# Получение заказов пользователя
@api.route('/orders', methods=['POST'])
def create_order():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]
    data = request.json

    if not data or 'orders' not in data:
        return jsonify({"message": "Invalid data"}), 400

    orders = data['orders']
    if not orders or not isinstance(orders, list):
        return jsonify({"message": "Orders should be a list"}), 400

    try:
        for order in orders:
            article = order.get('article')
            price = order.get('price')
            if not article or not price:
                return jsonify({"message": "Invalid order data"}), 400

            # Храним информацию о заказанных товарах в JSON-формате
            product_info = {
                "article": article,
                "price": price
            }

            query = f"""
                INSERT INTO orders (login, order_date, status, secret)
                VALUES (
                    '{username}', 
                    datetime('now'), 
                    'pending', 
                    '{json.dumps(product_info)}'
                )
            """
            execute_db(query)

        return jsonify({"message": "Orders placed successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating orders: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/orders', methods=['GET'])
def get_user_orders():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    query = f"""
        SELECT 
            orders.order_id,
            orders.order_date,
            orders.status
        FROM orders
        WHERE orders.login = '{username}'
    """

    try:
        orders = query_db(query)
        if not orders:
            return jsonify([]), 200  # Возвращаем пустой массив, если заказов нет
        orders_list = [
            {
                "order_id": row["order_id"],
                "order_date": row["order_date"],
                "status": row["status"]
            }
            for row in orders
        ]
        return jsonify(orders_list), 200
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return jsonify({"error": str(e)}), 500


# Получение избранных товаров
@api.route('/favorites', methods=['GET'])
def get_favorites():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized"}), 401

    username = auth_header.split(" ")[1]

    query = f"""
        SELECT 
            products.article, 
            products.name, 
            products.price, 
            products.category
        FROM favorite_products
        JOIN products ON favorite_products.article = products.article
        WHERE favorite_products.login = '{username}'
    """
    try:
        favorites = query_db(query)
        favorites_list = [dict(row) for row in favorites]
        return jsonify(favorites_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Регистрация Blueprint
app.register_blueprint(api)

# Запуск приложения
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
