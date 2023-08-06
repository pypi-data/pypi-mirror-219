from abc import (
    ABCMeta,
)
from typing import (
    Type,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from function_tools.managers import (
    RunnerManager,
)


class WebEduRunnerManager(RunnerManager, metaclass=ABCMeta):
    """
    Базовый класс менеджеров пускателей функций продуктов Образования.
    """

    @classmethod
    def _prepare_runner_class(cls) -> Type[WebEduRunner]:
        """
        Возвращает класс ранера.
        """
        return WebEduRunner

