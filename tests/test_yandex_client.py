import inspect

try:
    from app.core import yandex_client
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `yandex_client`. '
        'Проверьте и поправьте: он должен быть доступен в модуле `app.core`.',
    )


def test_yandex_disk_client_exists():
    assert hasattr(yandex_client, 'YandexDiskClient'), (
        'В файле `yandex_client` не обнаружен класс `YandexDiskClient`.'
    )


def test_yandex_disk_client_methods_exist():
    client_class = yandex_client.YandexDiskClient

    required_methods = [
        '__aenter__',
        '__aexit__',
        'create_excel_file',
        'upload_file',
        'publish_file',
        '_create_folder',
    ]

    missing_methods = [
        method for method in required_methods
        if not hasattr(client_class, method)
    ]

    assert not missing_methods, (
        'В классе `YandexDiskClient` не обнаружены следующие методы: '
        f'{", ".join(missing_methods)}.'
    )


def test_yandex_disk_client_methods_are_async():
    client_class = yandex_client.YandexDiskClient

    required_async_methods = [
        '__aenter__',
        '__aexit__',
        'create_excel_file',
        'upload_file',
        'publish_file',
        '_create_folder',
    ]

    not_async_methods = [
        method for method in required_async_methods
        if not inspect.iscoroutinefunction(getattr(client_class, method))
    ]

    assert not not_async_methods, (
        'Следующие методы класса `YandexDiskClient` должны быть '
        f'асинхронными: {", ".join(not_async_methods)}.'
    )


def test_get_yandex_client_exists():
    assert hasattr(yandex_client, 'get_yandex_client'), (
        'В файле `yandex_client` не обнаружена функция `get_yandex_client`.'
    )


def test_get_yandex_client_is_async_generator_function():
    assert inspect.isasyncgenfunction(yandex_client.get_yandex_client), (
        'Функция `get_yandex_client` должна быть асинхронным генератором.'
    )