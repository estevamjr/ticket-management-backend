from app.extensions import db
from app.models.user import User
from app.services.log import LogService
from app.utils.log import *

class UserService:
    
    @staticmethod
    def get_by_username(username: str) -> User:
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error fetching user by username: {e}")
            raise e
        
        
    @staticmethod
    def create_user(username: str, password: str) -> User:
        try:
            if User.query.filter_by(username=username).first():
                return None

            new_user = User(username=username)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            LogService.create_log(
                "CREATE_USER_SUCCESS", 
                f"User '{username}' created successfully."
            )
            return new_user
        except Exception as e:
            db.session.rollback()
            LogService.create_log("CREATE_USER_ERROR", f"Error creating user '{username}'. Exception: {e}")
            raise e