try:
    from app.core.config import settings
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект `settings` из модуля `app.core.config`.'
    )


def test_yandex_disk_token_exists():
    assert hasattr(settings, 'yandex_disk_token'), (
        'В классе `Settings` не обнаружено поле `yandex_disk_token`.'
    )


def test_report_format_exists():
    assert hasattr(settings, 'report_format'), (
        'В классе `Settings` не обнаружено поле `report_format`.'
    )


def test_report_format_default_value():
    assert settings.report_format, (
        'Поле `report_format` должно иметь значение по умолчанию.'
    )