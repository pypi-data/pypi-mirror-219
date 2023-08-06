from datetime import (
    date,
    datetime,
    time,
)
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Tuple,
)

from m3_db_utils.models import (
    ModelEnumValue,
)


if TYPE_CHECKING:
    from educommon.audit_log.models import (
        AuditLog,
    )


class BaseEduLogGenerator:
    """
    Базовый класс генератора логов для указанной модели РВД за определенный период времени.

    Для каждой модели РВД есть модели в продукте, создание экземпляров которых, сигнализирует о необходимости сбора
    и выгрузки данных в РВД. Модели можно найти в
    edu_rdm_integration/mapping.py MODEL_FIELDS_LOG_FILTER, принадлежность к конкретной
    модели РВД необходимо определять в функциях.
    """

    def generate(
        self,
        model: ModelEnumValue,
        logs_period_started_at: datetime = datetime.combine(date.today(), time.min),
        logs_period_ended_at: datetime = datetime.combine(date.today(), time.max),
        school_ids: Optional[Tuple[int]] = (),
    ) -> List['AuditLog']:
        """
        Возвращает список сгенерированных экземпляров модели AuditLog.

        Формирование логов производится для указанной модели РВД за указанный период времени.

        Args:
            model: значение модели РВД из модели-перечисления;
            logs_period_started_at: начало периода формирования логов;
            logs_period_ended_at: конец периода формирования логов;
            school_ids: список идентификаторов школ.
        """
        generate_logs_method = getattr(self, f'_generate_{model.key.lower()}_logs')

        logs = generate_logs_method(
            logs_period_started_at=logs_period_started_at,
            logs_period_ended_at=logs_period_ended_at,
            school_ids=school_ids,
        )

        return logs
