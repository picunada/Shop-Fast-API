from repositories.users import UserRepository
from db.connect import database

def get_user_repository() -> UserRepository:
    return UserRepository(database)