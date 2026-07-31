import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1812",
        database="fashion_ecommerce"
    )


def create_user(full_name, email, password):
    connection = get_connection()
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

    finally:
        cursor.close()
        connection.close()


def login_user(email, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s",
        (email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user