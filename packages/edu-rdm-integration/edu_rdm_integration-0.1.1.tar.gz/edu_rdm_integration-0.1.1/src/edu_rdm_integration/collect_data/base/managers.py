import logging
from abc import (
    ABCMeta,
)
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    List,
    Type,
)

from edu_rdm_integration.adapters.managers import (
    WebEduRunnerManager,
)
from edu_rdm_integration.consts import (
    DATETIME_FORMAT,
    LOGS_DELIMITER,
)
from edu_rdm_integration.models import (
    CollectingDataStageStatus,
    CollectingExportedDataStage,
)
from educommon.audit_log.helpers import (
    get_models_table_ids,
)
from educommon.audit_log.models import (
    AuditLog,
)
from function_tools.runners import (
    BaseRunner,
)


logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from django.db.models import (
        Model,
    )


class BaseCollectingDataRunnerManager(WebEduRunnerManager, metaclass=ABCMeta):
    """
    Базовый менеджер ранеров функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def __init__(
        self,
        logs_period_started_at: datetime,
        logs_period_ended_at: datetime,
        logs: List[AuditLog] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Логи для сущности
        self._logs = logs

        self._logs_period_started_at = logs_period_started_at

        logger.info(f'{LOGS_DELIMITER}logs period started at {self._logs_period_started_at.strftime(DATETIME_FORMAT)}')

        self._logs_period_ended_at = logs_period_ended_at

        logger.info(f'{LOGS_DELIMITER}log period ended at {self._logs_period_ended_at.strftime(DATETIME_FORMAT)}')

        self._stage = CollectingExportedDataStage.objects.create(
            manager_id=self.uuid,
            logs_period_started_at=logs_period_started_at,
            logs_period_ended_at=logs_period_ended_at,
        )

        logger.info(f'{LOGS_DELIMITER}created {repr(self._stage)}')

    def _collect_runner_regional_data_mart_integration_entities(
        self,
        runner_class: Type[BaseRunner],
        runner_regional_data_mart_integration_entities: List[str],
    ):
        """
        Собирает и возвращает список сущностей.
        """
        for runnable_class in runner_class._prepare_runnable_classes():
            if hasattr(runnable_class, '_prepare_runnable_classes'):
                self._collect_runner_regional_data_mart_integration_entities(
                    runner_class=runnable_class,
                    runner_regional_data_mart_integration_entities=runner_regional_data_mart_integration_entities,
                )

                continue

            if hasattr(runnable_class, 'entities'):
                entities = getattr(runnable_class, 'entities')

                runner_regional_data_mart_integration_entities.extend(entities)

    def _get_loggable_models(self) -> List['Model']:
        """
        Возвращает перечень моделей по которым собираются логи.
        """
        loggable_models = []
        regional_data_mart_integration_entities = []

        self._collect_runner_regional_data_mart_integration_entities(
            self.runner_class,
            regional_data_mart_integration_entities,
        )
        for entity in regional_data_mart_integration_entities:
            loggable_models.extend(entity.loggable_models)

        return loggable_models

    def _collect_logs(self):
        """
        Сбор логов для дальнейшей обработки.
        """
        return list(
            AuditLog.objects.filter(
                time__gte=self._logs_period_started_at,
                time__lte=self._logs_period_ended_at,
                table_id__in=get_models_table_ids(self._get_loggable_models()),
            ).order_by('time')
        )

    def _create_runner(self, *args, **kwargs):
        """
        Метод создания ранера.
        """
        collected_logs = self._logs or self._collect_logs()

        logger.info(
            f'{LOGS_DELIMITER}{self.__class__.__name__} start preparing {len(collected_logs) if collected_logs else 0} '
            f'logs records..'
        )

        super()._create_runner(logs=collected_logs, stage=self._stage, *args, **kwargs)

    def _before_start_runner(self, *args, **kwargs):
        """
        Точка расширения поведения менеджера ранера перед запуском ранера.
        """
        self._stage.status_id = CollectingDataStageStatus.IN_PROGRESS.key
        self._stage.save()

        logger.info(f'{LOGS_DELIMITER}change status {repr(self._stage)}')

    def _after_start_runner(self, *args, **kwargs):
        """
        Точка расширения поведения менеджера ранера после запуска ранера.
        """
        if self._runner.result.errors:
            self._stage.status_id = CollectingDataStageStatus.FAILED.key
        else:
            self._stage.status_id = CollectingDataStageStatus.FINISHED.key

        self._stage.save()

        logger.info(f'{LOGS_DELIMITER}change status {repr(self._stage)}')
