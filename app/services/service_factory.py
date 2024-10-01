from framework.services.service_factory import BaseServiceFactory
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
import os  # Optional: to use environment variables for sensitive data

class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'UserProfileResource':
            from app.resources.userprofile_resource import UserProfileResource
            return UserProfileResource(config=None)  # Assuming no config is needed
        elif service_name == 'UserProfileDataService':
            # You can replace hardcoded credentials with environment variables or secure config
            context = dict(
                user=os.getenv("DB_USER", "admin"),  # Use 'root' as default
                password=os.getenv("DB_PASSWORD", "dbuserdbuser"),  # Default to your current password
                host=os.getenv("DB_HOST", "user-micros-db.cdrum5qefv6d.us-east-1.rds.amazonaws.com"),  # Use your AWS RDS public endpoint
                port=int(os.getenv("DB_PORT", 3306))  # Default to MySQL port 3306
            )
            return MySQLRDBDataService(context=context)
        else:
            return None