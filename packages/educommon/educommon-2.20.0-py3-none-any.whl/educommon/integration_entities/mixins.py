from typing import (
    List,
)

from django.utils.decorators import (
    classproperty,
)


class EntitiesMixin:
    """
    Добавляет метод подготовки сущностей и свойства для доступа к ним.
    """

    # flake8: noqa: N805
    @classproperty
    def first_entity(cls) -> str:
        """
        Возвращает первый ключ модели-перечисления сущностей.
        """
        return cls._prepare_entities()[0]

    # flake8: noqa: N805
    @classproperty
    def entities(cls) -> List[str]:
        """
        Возвращает ключи модели-перечисления сущностей.
        """
        return cls._prepare_entities()

    @classmethod
    def _prepare_entities(cls) -> List[str]:
        """
        Формирование списка ключей модели-перечисления сущностей.
        """
        return []
