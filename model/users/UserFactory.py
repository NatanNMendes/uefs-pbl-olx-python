from models.natural_person import NaturalPerson
from models.legal_entity import LegalEntity
from utils.users_enum import UserType

class UserFactory:
    @staticmethod
    def create_user(user_type, *args):
        if user_type == UserType.NATURAL_PERSON:
            return NaturalPerson(*args)
        elif user_type == UserType.LEGAL_ENTITY:
            return LegalEntity(*args)
        else:
            raise ValueError("Invalid UserType")