from app.core.config import settings

MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1

MIN_DESCRIPTION_LENGTH = 10

FULL_AMOUNT_GT = 0

ROW_COUNT = 100
COLUMN_COUNT = 11

SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': 'Отчёт на {date}',
        'locale': 'ru_RU'
    },
    'sheets': [{'properties': {
        'sheetType': 'GRID',
        'sheetId': 0,
        'title': 'Лист1',
        'gridProperties': {
            'rowCount': ROW_COUNT,
            'columnCount': COLUMN_COUNT
        }}}]
}

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}