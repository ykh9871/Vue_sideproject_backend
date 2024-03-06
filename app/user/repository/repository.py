import mysql.connector

class UserRepository:
    def __init__(self):
        self.conn = mysql.connector.connect(
            port=3307,
            user="root",
            host="localhost",
            password="ykh9871",
            database="shoppingmall"
        )
        self.cursor= self.conn.cursor()

    def update_refresh_token(self, email: str, refresh_token: str):
        self.cursor.execute(
            "UPDATE customer "
            "SET refresh_token=%s "
            "WHERE Email=%s",
            (refresh_token, email)
        )
        self.conn.commit()