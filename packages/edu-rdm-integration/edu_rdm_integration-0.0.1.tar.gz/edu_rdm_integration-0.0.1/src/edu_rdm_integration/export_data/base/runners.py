import logging
from typing import (
    Type,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from edu_rdm_integration.export_data.base.helpers import (
    BaseExportDataRunnerHelper,
)
from edu_rdm_integration.export_data.base.results import (
    BaseExportDataRunnerResult,
)
from edu_rdm_integration.export_data.base.validators import (
    BaseExportDataRunnerValidator,
)


logger = logging.getLogger(__name__)


class BaseExportDataRunner(WebEduRunner):
    """
    Базовый класс ранеров функций выгрузки данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_helper_class(self) -> Type[BaseExportDataRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return BaseExportDataRunnerHelper

    def _prepare_validator_class(self) -> Type[BaseExportDataRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return BaseExportDataRunnerValidator

    def _prepare_result_class(self) -> Type[BaseExportDataRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return BaseExportDataRunnerResult

    def _prepare_model_ids_chunks(self, *args, model_ids_map=None, **kwargs):
        """
        Формирование чанков идентификаторов записей моделей для дальнейшей работы в рамках функций.
        """
        # model_ids_chunks = make_chunks(
        #     iterable=model_ids,
        #     size=RDM_EXPORT_CHUNK_SIZE,
        #     is_list=True,
        # )

        return ()

    def _populate_queue_by_runnable_classes(self, *args, **kwargs):
        """
        Заполнение очереди запускаемыми объектами.
        """
        model_ids_chunks = self._prepare_model_ids_chunks(*args, **kwargs)

        for chunk_index, model_ids_chunk in enumerate(model_ids_chunks, start=1):
            runnable_classes = self._prepare_runnable_classes()

            for runnable_class in runnable_classes:
                logger.info(
                    f'{LOGS_DELIMITER * 2}enqueue {runnable_class.__name__} with model ids chunk {chunk_index} with '
                    f'{len(model_ids_chunk)} records..'
                )

                runnable = runnable_class(model_ids=model_ids_chunk, *args, **kwargs)

                self.enqueue(runnable=runnable, *args, **kwargs)
