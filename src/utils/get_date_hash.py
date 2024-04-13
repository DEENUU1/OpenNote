from datetime import datetime


def get_date_hash() -> str:
    now = datetime.now()

    hashed = abs(hash(now))
    return str(hashed)
