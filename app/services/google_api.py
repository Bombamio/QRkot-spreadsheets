from datetime import datetime

from fastapi.concurrency import run_in_threadpool
from sqlalchemy import extract

from app.core.google_client import SHEETS_SERVICE

FORMAT = "%Y/%m/%d %H:%M:%S"


async def create_spreadsheets() -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    response = await run_in_threadpool(
        lambda: SHEETS_SERVICE.spreadsheets().create(
            body={
                'properties': {
                    'title': f'Отчёт на {now_date_time}',
                    'locale': 'ru_RU'
                },
                'sheets': [{'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': 100,
                        'columnCount': 11
                    }}}]

            }
        ).execute()
    )

    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def update_spreadsheets_value(
    spreadsheetid: str,
    projects: list,
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for prj in projects:
        new_row = [
            str(prj.name),
            str(
                (datetime.strftime(prj.close_date, FORMAT) -
                 datetime.strftime(prj.create_date, FORMAT))
            ),
            str(prj.description)
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await run_in_threadpool(
        lambda: SHEETS_SERVICE.spreadsheets().values().update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            body=update_body
        ).execute()
    )
