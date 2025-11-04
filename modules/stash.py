
### Handling Unittest 'stash' attribute that mimics pytest stash

from functools import wraps

def create_stashkey_safe():
    """
    Returns a new unique key for stashing.
    """
    return object()

def stash_get_safe(test, key):
    """
    Retrieves the stashed value for the given key from the test object, if present.
    """
    stash = getattr(test, '__allure_stash__', None)
    if stash and key in stash:
        return stash[key]
    return None

def stash_set_safe(test, key, value):
    """
    Sets a stashed value for the given key on the test object.
    """
    if not hasattr(test, '__allure_stash__'):
        setattr(test, '__allure_stash__', {})
    test.__allure_stash__[key] = value

def stashed(arg=None):
    """
    Caches the result of the decorated function in the test object's stash.
    The first argument of the function must be the test object.
    """
    key = create_stashkey_safe() if arg is None or callable(arg) else arg

    def decorator(func):
        @wraps(func)
        def wrapper(test, *args, **kwargs):
            if not hasattr(test, '__allure_stash__'):
                setattr(test, '__allure_stash__', {})
            stash = test.__allure_stash__
            if key in stash:
                return stash[key]
            value = func(test, *args, **kwargs)
            stash[key] = value
            return value
        return wrapper

    return decorator(arg) if callable(arg) else decorator