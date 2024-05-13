from datetime import datetime, timedelta


def get_today_date():
    return (datetime.now() - timedelta(hours=3)).date()
