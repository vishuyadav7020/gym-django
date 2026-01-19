from django.core.cache import cache

MAX_ATTEMPTS = 3
LOCK_TIME = 900  # 15 minutes (seconds)

def _attempt_key():
    return "global_login_attempts"

def _lock_key():
    return "global_login_lock"


def is_locked():
    return cache.get(_lock_key()) is not None


def record_failed_attempt():
    attempts = cache.get(_attempt_key(), 0) + 1
    cache.set(_attempt_key(), attempts, timeout=LOCK_TIME)

    if attempts >= MAX_ATTEMPTS:
        cache.set(_lock_key(), True, timeout=LOCK_TIME)
        return True, attempts

    return False, attempts


def reset_attempts():
    cache.delete(_attempt_key())
    cache.delete(_lock_key())