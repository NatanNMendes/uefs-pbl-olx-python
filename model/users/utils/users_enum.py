from enum import Enum

class UserType(Enum):
    LEGAL_ENTITY = "LEGAL_ENTITY"
    NATURAL_PERSON = "NATURAL_PERSON"
    ADMIN = "ADMIN"
    DEFAULT = "DEFAULT"