from enum import EnumMeta, Enum, IntFlag
from datetime import datetime, timezone
from typing import Any
from dataclasses import dataclass

from typing_utils import issubtype

def is_high_model_type(type_):
    """
    Whether ``type_`` is both a model type and not a base model type.

    "high" here is meant to indicate that it is not at the bottom of the model
    hierarchy, ie not a "base" model.
    """
    return is_model_type(type_) and not is_base_model_type(type_)

def is_model_type(type_):
    """
    Whether ``type_`` is a subclass of ``Model``.
    """
    if not isinstance(type_, type):
        return False
    return issubclass(type_, Model)

def is_base_model_type(type_):
    """
    Whether ``type_`` is a subclass of ``BaseModel``.
    """
    if not isinstance(type_, type):
        return False
    return issubclass(type_, BaseModel)


class Field:
    def __init__(self, *, name=None):
        self.name = name


class _Model:
    """
    Base class for all models in ``ossapi``. If you want a model which handles
    its own members and cleanup after instantion, subclass ``BaseModel``
    instead.
    """
    def override_types(self):
        """
        Sometimes, the types of attributes in models depends on the value of
        other fields in that model. By overriding this method, models can return
        "override types", which overrides the static annotation of attributes
        and tells ossapi to use the returned type to instantiate the attribute
        instead.

        This method should return a mapping of ``attribute_name`` to
        ``intended_type``.
        """
        return {}

    @classmethod
    def override_class(cls, _data):
        """
        This method addressess a shortcoming in ``override_types`` in order to
        achieve full coverage of the intended feature of overriding types.

        The model that we want to override types for may be at the very top of
        the hierarchy, meaning we can't go any higher and find a model for which
        we can override ``override_types`` to customize this class' type.

        A possible solution for this is to create a wrapper class one step above
        it; however, this is both dirty and may not work (I haven't actually
        tried it). So this method provides a way for a model to override its
        *own* type (ie class) at run-time.
        """
        return None

class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        model = super().__new__(cls, name, bases, dct)
        field_names = []
        for name, value in model.__dict__.items():
            if name.startswith("__") and name.endswith("__"):
                continue
            if isinstance(value, Field):
                field_names.append(name)

        for name in model.__annotations__:
            if name in field_names:
                continue
            setattr(model, name, None)

        return dataclass(model)

class Model(_Model, metaclass=ModelMeta):
    """
    A dataclass-style model. Provides an ``_api`` attribute.
    """
    # This is the ``OssapiV2`` instance that loaded this model.
    # can't annotate with OssapiV2 or we get a circular import error, this is
    # good enough.
    _api: Any

    def _foreign_key(self, fk, func, existing):
        if existing:
            return existing
        if fk is None:
            return None
        return func()

    def _fk_user(self, user_id, existing=None):
        func = lambda: self._api.user(user_id)
        return self._foreign_key(user_id, func, existing)

    def _fk_beatmap(self, beatmap_id, existing=None):
        func = lambda: self._api.beatmap(beatmap_id)
        return self._foreign_key(beatmap_id, func, existing)

    def _fk_beatmapset(self, beatmapset_id, existing=None):
        func = lambda: self._api.beatmapset(beatmapset_id)
        return self._foreign_key(beatmapset_id, func, existing)

class BaseModel(_Model):
    """
    A model which promises to take care of its own members and cleanup, after we
    instantiate it.

    Normally, for a high (non-base) model type, we recurse down its members to
    look for more model types after we instantiate it. We also resolve
    annotations for its members after instantion. None of that happens with a
    base model; we hand off the model's data to it and do nothing more.

    A commonly used example of a base model type is an ``Enum``. Enums have
    their own magic that takes care of cleaning the data upon instantiation
    (taking a string and converting it into one of a finite set of enum members,
    for instance). We don't need or want to do anything else with an enum after
    instantiating it, hence it's defined as a base type.
    """
    pass

class EnumModel(BaseModel, Enum):
    pass

class IntFlagModel(BaseModel, IntFlag):
    pass


class Datetime(datetime, BaseModel):
    """
    Our replacement for the ``datetime`` object that deals with the various
    datetime formats the api returns.
    """
    def __new__(cls, value): # pylint: disable=signature-differs
        if value is None:
            raise ValueError("cannot instantiate a Datetime with a null value")
        # the api returns a bunch of different timestamps: two ISO 8601
        # formats (eg "2018-09-11T08:45:49.000000Z" and
        # "2014-05-18T17:22:23+00:00"), a unix timestamp (eg
        # 1615385278000), and others. We handle each case below.
        # Fully compliant ISO 8601 parsing is apparently a pain, and
        # the proper way to do this would be to use a third party
        # library, but I don't want to add any dependencies. This
        # stopgap seems to work for now, but may break in the future if
        # the api changes the timestamps they return.
        # see https://stackoverflow.com/q/969285.
        if value.isdigit():
            # see if it's an int first, if so it's a unix timestamp. The
            # api returns the timestamp in milliseconds but
            # ``datetime.fromtimestamp`` expects it in seconds, so
            # divide by 1000 to convert.
            value = int(value) / 1000
            return datetime.fromtimestamp(value, tz=timezone.utc)
        if cls._matches_datetime(value, "%Y-%m-%dT%H:%M:%S.%f%z"):
            return value
        if cls._matches_datetime(value, "%Y-%m-%dT%H:%M:%S%z"):
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        if cls._matches_datetime(value, "%Y-%m-%d"):
            return datetime.strptime(value, "%Y-%m-%d")
        raise ValueError(f"invalid datetime string {value}")

    @staticmethod
    def _matches_datetime(value, format_):
        try:
            _ = datetime.strptime(value, format_)
        except ValueError:
            return False
        return True



# typing utils
# ------------

def is_optional(type_):
    """
    Whether ``type(None)`` is a valid instance of ``type_``. eg,
    ``is_optional(Union[str, int, NoneType]) == True``.

    Exception: when ``type_`` is any, we return false. Strictly speaking, if
    ``Any`` is a subtype of ``type_`` then we return false, since
    ``Union[Any, str]`` is a valid type not equal to ``Any`` (in python), but
    representing the same set of types.
    """
    return issubtype(type(None), type_) and not issubtype(Any, type_)

def is_primitive_type(type_):
    if not isinstance(type_, type):
        return False
    return type_ in [int, float, str, bool]

def is_compatible_type(value, type_):
    # make an exception for an integer being instantiated as a float. In
    # the json we receive, eg ``pp`` can have a value of ``15833``, which is
    # interpreted as an int by our json parser even though ``pp`` is a
    # float.
    if type_ is float and isinstance(value, int):
        return True
    return isinstance(value, type_)
