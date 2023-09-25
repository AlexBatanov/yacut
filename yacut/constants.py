import string


# created custom link
CHARACTERS = list(
    string.ascii_uppercase + string.ascii_lowercase + string.digits
)
MAX_LEN_LINK = 6
NUM_URL_PARTS = 3

# forms validates
MAX_CUSTOM_ID = 16
MIN_LEN_LINK = 1

# error masseges
NOT_CORRECT_NAME_LINK = 'Указано недопустимое имя для короткой ссылки'
REQUERED_URL_FIELD = '"url" является обязательным полем!'
DATA_NOT = 'Отсутствует тело запроса'


def name_is_ocuppet(custom_id, api=False):
    if api:
        return f'Имя "{custom_id}" уже занято.'
    return f'Имя {custom_id} уже занято!'
