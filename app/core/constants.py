# db constraints

class UserDBConstants:
    USERNAME_LEN = 64
    FIRST_NAME_LEN = 32
    LAST_NAME_LEN = 64
    EMAIL_LEN = 254
    PASSWORD_LEN = 32
    AVATAR_URL_LEN = 220


class VehicleDBConstants:
    VEHICLE_NAME_LEN = 254
    VEHICLE_DESC_LEN = 500
    IMAGE_URL_LEN = 220


class CategoryDBConstants:
    CATEGORY_NAME_LEN = 50
    CATEGORY_DESC_LEN = 500


class TagDBConstants:
    TAG_NAME_LEN = 30
    TAG_DESC_LEN = 500


# schemas constraints
class CategorySchemaConstants:
    MIN_NAME_LEN = 5
    MAX_NAME_LEN = 254


class TagSchemaConstants:
    MIN_NAME_LEN = 5
    MAX_NAME_LEN = 254


class VehicleSchemaConstants:
    MIN_NAME_LEN = 2
    MAX_NAME_LEN = 254


class UserSchemaConstants:
    MIN_USERNAME_LEN = 2
    MAX_USERNAME_LEN = 64
    USERNAME_PATTERN = r'^[a-zA-Z0-9_-]+$'

    MIN_FN_LEN = 2
    MAX_FN_LEN = 128

    MIN_LN_LEN = 2
    MAX_LN_LEN = 128

    MIN_EMAIL_LEN = 8
    MAX_EMAIL_LEN = 254

    MIN_PWD_LEN = 8
    MAX_PWD_LEN = 64
    PWD_ERR_MESSAGE = 'Пароли не совпадают'