import sqlite3

def populate_database():
    conn = sqlite3.connect('clothesshop.db')
    c = conn.cursor()

    # Добавляем данные в таблицу users
    c.executemany('''
        INSERT INTO users (login, password, role) VALUES (?, ?, ?)
    ''', [
        ('admin', 'admin123', 'admin'),
        ('user1', 'password1', 'customer'),
        ('user2', 'password2', 'customer')
    ])

    # Добавляем данные в таблицу user_personal_info
    c.executemany('''
        INSERT INTO user_personal_info (login, name, birth_date, address, phone_number, secret)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        ('user1', 'Alice Johnson', '1990-01-01', '123 Main St, Cityville', '555-1234', 'secret1'),
        ('user2', 'Bob Smith', '1992-05-15', '456 Elm St, Townsville', '555-5678', 'secret2')
    ])

    # Добавляем данные в таблицу product_categories
    c.executemany('''
        INSERT INTO product_categories (category, higher_category, secret)
        VALUES (?, ?, ?)
    ''', [
        ('T-Shirts', 'Clothing', 'secret3'),
        ('Jeans', 'Clothing', 'secret4'),
        ('Sneakers', 'Footwear', 'secret5')
    ])

    # Добавляем данные в таблицу products
    c.executemany('''
        INSERT INTO products (article, description, name, category, price, stock, released, secret)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1001, 'Classic white T-shirt', 'White T-Shirt', 'T-Shirts', 19.99, 100, 1, 'secret6'),
        (1002, 'Comfortable blue jeans', 'Blue Jeans', 'Jeans', 49.99, 50, 1, 'secret7'),
        (1003, 'Stylish running sneakers', 'Running Sneakers', 'Sneakers', 79.99, 30, 1, 'secret8')
    ])

    # Добавляем данные в таблицу orders
    c.executemany('''
        INSERT INTO orders (order_id, login, order_date, status, secret)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, 'user1', '2024-01-01 10:00:00', 'completed', 'secret9'),
        (2, 'user2', '2024-01-02 14:30:00', 'pending', 'secret10')
    ])

    # Добавляем данные в таблицу reviews
    c.executemany('''
        INSERT INTO reviews (review_id, login, article, rating, review_text, review_date, secret)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1, 'user1', 1001, 5, 'Great quality T-shirt!', '2024-01-01 12:00:00', 'secret11'),
        (2, 'user2', 1002, 4, 'Nice jeans, but a bit expensive.', '2024-01-02 15:00:00', 'secret12')
    ])

    # Добавляем данные в таблицу shipping_addresses
    c.executemany('''
        INSERT INTO shipping_addresses (address_id, login, country, city, street, postal_code, secret)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (1, 'user1', 'USA', 'Cityville', '123 Main St', '12345', 'secret13'),
        (2, 'user2', 'USA', 'Townsville', '456 Elm St', '67890', 'secret14')
    ])

    # Добавляем данные в таблицу payments
    c.executemany('''
        INSERT INTO payments (order_id, payment_method, amount, payment_status, secret)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, 'Credit Card', 19.99, 'Paid', 'secret15'),
        (2, 'PayPal', 49.99, 'Pending', 'secret16')
    ])

    # Добавляем данные в таблицу favorite_products
    c.executemany('''
        INSERT INTO favorite_products (login, article, added_date, secret)
        VALUES (?, ?, ?, ?)
    ''', [
        ('user1', 1001, '2024-01-01 13:00:00', 'secret17'),
        ('user2', 1002, '2024-01-02 16:00:00', 'secret18')
    ])

    # Добавляем данные в таблицу price_history
    c.executemany('''
        INSERT INTO price_history (history_id, product_article, old_price, new_price, changed_date, secret)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (1, 1001, 18.99, 19.99, '2023-12-31 23:59:59', 'secret19'),
        (2, 1002, 45.99, 49.99, '2023-12-31 23:59:59', 'secret20')
    ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_database()
