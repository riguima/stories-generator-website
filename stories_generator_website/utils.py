from datetime import datetime

from pytz import timezone


def get_today_date():
    return datetime.now(timezone('America/Sao_Paulo')).date()
