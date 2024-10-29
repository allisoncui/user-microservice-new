import os
import pymysql
import logging
from framework.resources.base_resource import BaseResource
from app.models.user_profile import UserProfile
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserProfileResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        self.table = "Profile"

    def get_db_connection(self):
        """Establish connection to the MySQL database."""
        return pymysql.connect(**self.db_config)

    def register_user(self, username: str) -> int:
        """Register user if not already registered."""
        query_check = f"SELECT user_id FROM {self.table} WHERE username = %s"
        query_insert = f"INSERT INTO {self.table} (username) VALUES (%s)"

        connection = self.get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Check if the user exists
                cursor.execute(query_check, (username,))
                user = cursor.fetchone()

                if user:
                    logging.info(f"User '{username}' already exists.")
                    return user[0]

                # Insert a new user profile
                cursor.execute(query_insert, (username,))
                connection.commit()
                logging.info(f"User '{username}' registered successfully.")
                return cursor.lastrowid
        finally:
            connection.close()

    def get_by_key(self, username: str) -> UserProfile:
        """Retrieve user profile by the username key."""
        query = f"SELECT * FROM {self.table} WHERE username = %s"

        connection = self.get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result:
                    return UserProfile(**result)
                else:
                    return None
        finally:
            connection.close()

    def get_viewed_restaurants(self, username: str) -> list:
        """Retrieve the viewed restaurants of a user."""
        query = f"SELECT viewed_restaurants FROM {self.table} WHERE username = %s"

        connection = self.get_db_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result and result.get("viewed_restaurants"):
                    return result["viewed_restaurants"].split(",")
                else:
                    return []
        finally:
            connection.close()
