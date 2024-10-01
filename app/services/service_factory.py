import os
from framework.services.service_factory import BaseServiceFactory
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService

class ServiceFactory(BaseServiceFactory):

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'UserProfileResource':
            from app.resources.userprofile_resource import UserProfileResource
            return UserProfileResource(config=None)
        elif service_name == 'UserProfileDataService':
            context = {
                'user': os.getenv("DB_USER", "root"),
                'password': os.getenv("DB_PASSWORD", "dbuserdbuser"),
                'host': os.getenv("DB_HOST", "availability-database.cb821k94flru.us-east-1.rds.amazonaws.com"),
                'port': int(os.getenv("DB_PORT", 3306))
            }
            return MySQLRDBDataService(context=context)
        else:
            return None