import logging

logger = logging.getLogger(__name__)


class UnCallableException(Exception):
    pass


class Register:
    """ Register apscheduler

    """

    def __init__(self):
        self._dict = {}

    def register(self, target):
        """ register a function

        param: target func
        """

        def add_register_item(key, value):
            if not callable(value):
                raise UnCallableException(f"Register object must be callable, "
                                          f"but receive:{value} is not callable!")
            if key in self._dict:
                logger.warning(
                    '%s has been registered before, so we will overriden it', value.__name__
                )
            self._dict[key] = value

            return value

        if callable(target):
            # If the passed target is callable, we use the name of the passed function or class
            # as the registration name if no registration name was previously given.
            return add_register_item(target.__name__, target)

        return lambda x: add_register_item(target, x)

    def __call__(self, target):
        return self.register(target)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()


aps_register = Register()
