from abc import ABC, abstractmethod
from utils.location import Location

class Users(ABC):
    id_counter = 1

    def __init__(self, name, user_name, email, vat, age, postal_code):
        self.id = Users.id_counter
        Users.id_counter += 1
        self.name = name
        self.user_name = user_name
        self.email = email
        self.vat = vat
        self.age = age
        self.location  = Location(postal_code)