import sqlite3

def create_database():
    conn = sqlite3.connect('clothesshop.db')
    c = conn.cursor()

    # Таблица users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            login VARCHAR(100) NOT NULL PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    ''')

    # Таблица user_personal_info
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_personal_info (
            login VARCHAR(100) NOT NULL,
            name VARCHAR(100) NOT NULL,
            birth_date DATE NOT NULL,
            address TEXT NOT NULL,
            phone_number VARCHAR(50) NOT NULL,
            secret VARCHAR(40),
            PRIMARY KEY (login),
            FOREIGN KEY (login) REFERENCES users (login)
        )
    ''')

    # Таблица product_categories
    c.execute('''
        CREATE TABLE IF NOT EXISTS product_categories (
            category VARCHAR(100) NOT NULL PRIMARY KEY,
            higher_category VARCHAR(100) NOT NULL,
            secret VARCHAR(40)
        )
    ''')

    # Таблица products
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            article BIGINT NOT NULL PRIMARY KEY,
            description TEXT NOT NULL,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            stock INT NOT NULL,
            released BOOLEAN NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (category) REFERENCES product_categories (category)
        )
    ''')

    # Таблица orders
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id BIGINT NOT NULL PRIMARY KEY,
            login VARCHAR(100) NOT NULL,
            order_date TIMESTAMP NOT NULL,
            status VARCHAR(50) NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (login) REFERENCES users (login)
        )
    ''')

    # Таблица reviews
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id BIGINT NOT NULL PRIMARY KEY,
            login VARCHAR(100) NOT NULL,
            article BIGINT NOT NULL,
            rating INT NOT NULL,
            review_text TEXT NOT NULL,
            review_date TIMESTAMP NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (login) REFERENCES users (login),
            FOREIGN KEY (article) REFERENCES products (article)
        )
    ''')

    # Таблица shipping_addresses
    c.execute('''
        CREATE TABLE IF NOT EXISTS shipping_addresses (
            address_id BIGINT NOT NULL PRIMARY KEY,
            login VARCHAR(100) NOT NULL,
            country VARCHAR(100) NOT NULL,
            city VARCHAR(100) NOT NULL,
            street VARCHAR(100) NOT NULL,
            postal_code VARCHAR(50) NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (login) REFERENCES users (login)
        )
    ''')

    # Таблица payments
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            order_id BIGINT NOT NULL PRIMARY KEY,
            payment_method VARCHAR(50) NOT NULL,
            amount NUMERIC(10, 2) NOT NULL,
            payment_status VARCHAR(50) NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')

    # Таблица favorite_products
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorite_products (
            login VARCHAR(100) NOT NULL,
            article BIGINT NOT NULL,
            added_date TIMESTAMP NOT NULL,
            secret VARCHAR(40),
            PRIMARY KEY (login, article),
            FOREIGN KEY (login) REFERENCES users (login),
            FOREIGN KEY (article) REFERENCES products (article)
        )
    ''')

    # Таблица price_history
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            history_id BIGINT NOT NULL PRIMARY KEY,
            product_article BIGINT NOT NULL,
            old_price NUMERIC(10, 2) NOT NULL,
            new_price NUMERIC(10, 2) NOT NULL,
            changed_date TIMESTAMP NOT NULL,
            secret VARCHAR(40),
            FOREIGN KEY (product_article) REFERENCES products (article)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
