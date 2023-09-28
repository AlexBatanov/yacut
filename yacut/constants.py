import string


# created custom link
CHARACTERS = list(
    string.ascii_uppercase + string.ascii_lowercase + string.digits
)
MAX_LEN_LINK = 6
NUM_URL_PARTS = 3
PATTERN = r'^[a-zA-Z0-9]+$'

# forms validates
MAX_CUSTOM_ID = 16
MIN_LEN_LINK = 1

# error masseges
NOT_CORRECT_NAME_LINK = 'Указано недопустимое имя для короткой ссылки'
REQUERED_URL_FIELD = '"url" является обязательным полем!'
DATA_NOT = 'Отсутствует тело запроса'
NOT_UNICUE_CUSTOM_ID = 'Имя {0} уже занято!'
NOT_UNICUE_CUSTOM_ID_API = 'Имя "{0}" уже занято.'
