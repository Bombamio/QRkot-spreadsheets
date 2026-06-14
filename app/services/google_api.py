from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi.concurrency import run_in_threadpool

from app.core.google_client import SHEETS_SERVICE
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


# OAuth 2.0
async def create_spreadsheets_oauth() -> str:
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


# OAuth 2.0
async def update_spreadsheets_value_oauth(
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
            str(prj.close_date - prj.create_date),
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


# Service Account
async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
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
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


# Service Account
async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


# Service Account
async def update_spreadsheets_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for prj in projects:
        new_row = [
            str(prj.name),
            str(prj.close_date - prj.create_date),
            str(prj.description)
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
