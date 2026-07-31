import mysql.connector


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1812",
            database="fashion_ecommerce"
        )
    except Exception:
        return None


def create_user(full_name, email, password):
    connection = get_connection()
    if not connection:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
            (full_name, email, password)
        )
        connection.commit()
        return True

    except mysql.connector.IntegrityError:
        return False
    except Exception:
        return False

    finally:
        cursor.close()
        connection.close()


def login_user(email, password):
    connection = get_connection()
    if not connection:
        return None

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        return user
    except Exception:
        return None
    finally:
        cursor.close()
        connection.close()