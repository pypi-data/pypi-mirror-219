"""Base updaters module."""

import contextlib
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from fastapi_jsonapi.querystring import HeadersQueryStringManager

from .exceptions import (
    ExceptionBeforeUpdate,
    ExceptionNotUpdater,
    ObjectNotFound,
)

Base = declarative_base()

TypeModel = TypeVar("TypeModel", bound=Base)
empty = object()


class _BaseUpdater(Generic[TypeModel]):
    class Meta(object):
        model: Any

    @classmethod
    async def update(
        cls,
        model_or_id: Union[TypeModel, int],
        new_data: Dict[str, Any],
        header: Union[HeadersQueryStringManager, None] = None,
        save: bool = True,
        update_fields: Optional[Iterable[str]] = None,
        session: Optional[AsyncSession] = None,
    ) -> TypeModel:
        """
        Create objects.

        :param cls: updater
        :param new_data: named parameters for the updater
        :param model_or_id: object or id
        :param header: header
        :param save: boolean flag: model saved to db or not
        :param update_fields:
        :param session:
        :return: created model.
        """
        model_obj = await cls._preload_model(model_or_id, session)

        with contextlib.suppress(ExceptionBeforeUpdate):
            model_obj = await cls.before_update(obj=model_obj, new_data=new_data, header=header)

        if save:
            if session:
                await session.commit()
            else:
                await model_obj.save(update_fields=update_fields)

        return model_obj

    @classmethod
    async def _preload_model(cls, model_or_id: Union[TypeModel, int], session: AsyncSession) -> TypeModel:
        """
        Preload model method.

        If updater initialize with int id - load from database with this id.
        :return: Model. Returns model from initialization or preloaded model.
        :raises ObjectNotFound: if object does not found.
        """
        if isinstance(model_or_id, int):
            try:
                stmt = select(cls.Meta.model).where(cls.Meta.model.id == model_or_id)
                model_instance = (await session.execute(stmt)).scalar_one()
            except NoResultFound:
                raise ObjectNotFound(cls.Meta.model, description="Object does not exist")

            return model_instance
        else:
            return model_or_id

    @classmethod
    async def before_update(
        cls,
        obj: TypeModel,
        new_data: Dict[Any, Any],
        header: Union[HeadersQueryStringManager, None] = None,
    ) -> TypeModel:
        """
        Perform logic before the updater starts.

        :param obj: argument with preloaded model,
        :param new_data: argument with new data
        :param header: header
        :return: named parameters to update an object
        :raises ExceptionBeforeUpdate: if 'before_update' has failed.
        """
        raise ExceptionBeforeUpdate


class Updaters:
    """Updaters factory."""

    _updaters: Dict[str, Type["_BaseUpdater"]] = {}

    @classmethod
    def get(cls, name_model: str) -> Type["_BaseUpdater"]:
        """Get updater from storage."""
        try:
            return cls._updaters[name_model]
        except KeyError:
            msg = "Not found updater={model}".format(model=name_model)
            raise ExceptionNotUpdater(msg)

    @classmethod
    def add(cls, name_updater: str, updater: Type["_BaseUpdater"]) -> None:
        """Add to storage method."""
        cls._updaters[name_updater] = updater


class MetaUpdater(type):
    """Metaclass for updater."""

    def __new__(cls, name, bases, attrs):
        """Create updater instance and add it to storage."""
        updater = super().__new__(cls, name, bases, attrs)
        if issubclass(updater, _BaseUpdater):
            Updaters.add(name, updater)
        return updater


class BaseUpdater(_BaseUpdater, metaclass=MetaUpdater):
    """Base updater."""

    @classmethod
    def _update_field_if_present_and_new(
        cls,
        obj: TypeModel,
        new_data: Dict[str, Any],
        field: str,
        field_data: str = empty,
    ) -> None:
        if field_data is empty:
            field_data = field

        if field_data not in new_data:
            return

        value = Optional[Any] = new_data.get(field_data)
        if value != getattr(obj, field):
            setattr(obj, field, value)
