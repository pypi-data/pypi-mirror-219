import os
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
)

from django.conf import (
    settings,
)

from edu_rdm_integration.apps import (
    EduRDMIntegrationConfig,
)


if TYPE_CHECKING:
    from edu_rdm_integration.models import (
        BaseEntityModel,
    )


def get_exporting_data_stage_attachment_path(instance, filename):
    """Возвращает путь до файла-вложения в этап выгрузки данных сущности.

    Args:
        instance: объект ExportingDataStage
        filename: имя загружаемого файла

    Returns:
        Строковое представление пути
    """
    datetime_now = datetime.now()

    return os.path.join(
        settings.UPLOADS,
        EduRDMIntegrationConfig.label,
        datetime_now.strftime('%Y/%m/%d'),
        instance.exporting_data_sub_stage.__class__.__name__.lower(),
        str(instance.exporting_data_sub_stage_id),
        str(instance.operation),
        filename,
    )


def update_fields(
    entity: 'BaseEntityModel',
    field_values: Dict[str, Any],
    mapping: Dict[str, str]
) -> None:
    """Обновление значений полей сущности по измененным полям модели.

    :param entity: Выгружаемая сущность
    :param field_values: Словарь с измененными данными модели
    :param mapping: Словарь маппинга полей модели к полям сущности
    """
    for model_field, entity_field in mapping.items():
        if model_field in field_values:
            setattr(entity, entity_field, field_values[model_field])


def get_isoformat_timezone():
    """Возвращает временную зонну в ISO представлении."""
    return datetime.now().astimezone().isoformat()[-6:]
