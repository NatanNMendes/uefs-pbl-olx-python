from users import Users
from utils.users_enum import *

class LegalEntity(Users):
    def __init__(self, name, user_name, email, vat, age, postal_code):
        super().__init__(name, user_name, email, vat, age, postal_code)
        self.user_type = UserType.NATURAL_PERSON