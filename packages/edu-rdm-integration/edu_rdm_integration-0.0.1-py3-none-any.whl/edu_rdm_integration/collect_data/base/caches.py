from typing import (
    Any,
    Dict,
    Optional,
)

from edu_rdm_integration.adapters.caches import (
    WebEduEntityCache,
)


class WebEduEntityCacheExtended(WebEduEntityCache):
    """
    Расширенный класс для кэша сущностей ЭШ.

    Добавлена поддержка annotation и exclude
    """

    def __init__(
        self,
        additional_exclude_params: Optional[Dict[str, Any]] = None,
        annotated_fields: Optional[Dict] = None,
        *args,
        **kwargs
    ):
        self._additional_exclude_params = additional_exclude_params or {}
        self._annotated_fields = annotated_fields

        super().__init__(*args, **kwargs)

    def _prepare_entities(self):
        """
        Получение выборки объектов модели по указанными параметрам.
        """
        self._entities = self._actual_entities_queryset.filter(
            **self._additional_filter_params,
        ).exclude(**self._additional_exclude_params)

        if self._annotated_fields:
            self._entities = self._entities.annotate(**self._annotated_fields)

        if self._only_fields:
            self._entities = self._entities.only(*self._only_fields)

        self._entities = self._entities.distinct()
