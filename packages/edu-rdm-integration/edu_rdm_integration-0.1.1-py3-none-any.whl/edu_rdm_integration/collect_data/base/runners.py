import logging

from django.conf import (
    settings,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from educommon.utils.seqtools import (
    make_chunks,
)


logger = logging.getLogger(__name__)



class BaseCollectingCalculatingDataRunner(WebEduRunner):
    """
    Базовый класс ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _populate_queue_by_runnable_classes(self, logs, *args, **kwargs):
        """
        Заполнение очереди запускаемыми объектами.
        """
        raw_logs_chunks = make_chunks(
            iterable=logs,
            size=settings.RDM_COLLECT_CHUNK_SIZE,
            is_list=True,
        )

        for chunk_index, raw_logs in enumerate(raw_logs_chunks, start=1):
            runnable_classes = self._prepare_runnable_classes()

            for runnable_class in runnable_classes:
                logger.info(
                    f'{LOGS_DELIMITER*2}enqueue {runnable_class.__name__} with logs chunk {chunk_index} with '
                    f'{len(raw_logs)} records..'
                )

                runnable = runnable_class(raw_logs=raw_logs, *args, **kwargs)

                self.enqueue(runnable=runnable, *args, **kwargs)
