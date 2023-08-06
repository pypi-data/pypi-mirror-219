import logging
import yaml

Logger = logging.getLogger('mlky/registers')


class Null:
    """
    Null class. Used by Section to access nonexistant keys without raising an exception.
    Can be set in the config using the value `mlky.Null` which allows optional
    keys to exist in the config without using `null` which would set the key as
    a NoneType therefore potentially causing exceptions during runtime.
    """
    # Register mlky.Null with pyyaml to auto convert into the Null object
    # yaml.add_constructor(u'mlky.Null', lambda *args: Null())
    # yaml.add_implicit_resolver(u'mlky.Null', re.compile(r'mlky\.Null'))
    # TODO: Maybe ${Null} replacement?

    def __call__(self, *args, **kwargs):
        ...

    def __deepcopy__(self, memo):
        return type(self)()

    def __bool__(self):
        return False

    def __eq__(self, other):
        if type(other) in [type(None), type(self)]:
            return True
        return False

    def __getattr__(self, key):
        return self

    def __getitem__(self, key):
        return self

    def __contains__(self):
        return False

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def __repr__(self):
        return 'Null'

    def __str__(self):
        return 'Null'

    def get(self, key, other=None):
        return other

    def keys(self):
        return []


class Register:
    """
    Object type to store boolean functions to be applied to Variables
    """
    funcs = {}

    @classmethod
    def check(cls, key, value):
        ...

    @classmethod
    def register(cls, key, func, example=None):
        """
        Registers a custom function to be used by the `check` function
        implemented by the subclass.

        Additionally protects from exceptions.
        """
        def protect(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                Logger.exception(f'Function {key} from register {cls.__name__} raised an exception:')
                False

        cls.funcs[key] = protect


class Functions(Register):
    @classmethod
    def check(cls, key, val, **kwargs):
        """
        """
        if key not in cls.funcs:
            return 'Check not registered'
        return cls.funcs[key](val, **kwargs)


class Types(Register):
    funcs = {
        Null     : lambda value: True,
        'Null'   : lambda value: True,
        None     : lambda value: True,
        'None'   : lambda value: True,
        'any'    : lambda value: True,
        'bool'   : lambda value: isinstance(value, bool   ),
        'bytes'  : lambda value: isinstance(value, bytes  ),
        'complex': lambda value: isinstance(value, complex),
        'dict'   : lambda value: isinstance(value, dict   ),
        'float'  : lambda value: isinstance(value, float  ),
        'int'    : lambda value: isinstance(value, int    ),
        'list'   : lambda value: isinstance(value, list   ),
        'set'    : lambda value: isinstance(value, set    ),
        'str'    : lambda value: isinstance(value, str    ),
        'tuple'  : lambda value: isinstance(value, tuple  )
    }

    @classmethod
    def check(cls, dtype, value):
        if isinstance(dtype, list):
            return any([cls.funcs.get(t)(value) for t in dtype])
        return bool(cls.funcs.get(dtype)(value))


def register(kind, key=None):
    def decorator(function):
        registers = {
            'type'    : Types,
            'function': Functions
        }
        if kind in registers:
            registers[kind].register(key or function.__name__, function)
        else:
            Logger.error(f'Invalid register kind: {kind!r}, must be one of: {registers.keys()}')
        return function
    return decorator
