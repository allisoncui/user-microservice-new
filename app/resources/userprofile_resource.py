import pymysql
from framework.resources.base_resource import BaseResource
from app.models.user_profile import UserProfile

class UserProfileResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        # MySQL database connection details (adjust based on your AWS RDS instance)
        self.db_config = {
            'host': 'user-micros-db.cdrum5qefv6d.us-east-1.rds.amazonaws.com',  # Replace with your AWS RDS endpoint
            'user': 'admin',  # Replace with your MySQL username
            'password': 'dbuserdbuser',  # Replace with your MySQL password
            'database': 'user_db',  # Replace with your database name
            'port': 3306  # Default MySQL port
        }
        self.table = "users"  # The MySQL table to query

    def get_db_connection(self):
        """Establish connection to the MySQL database."""
        return pymysql.connect(**self.db_config)

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
                    # Assuming `viewed_restaurants` is a comma-separated string
                    return result["viewed_restaurants"].split(",")
                else:
                    return []
        finally:
            connection.close()