from edu_rdm_integration.management.general import (
    BaseCollectModelDataCommand,
)


class Command(BaseCollectModelDataCommand):
    """
    Команда для сбора данных моделей РВД за указанных период по существующим логам.
    """

    # flake8: noqa: A003
    help = 'Команда для сбора данных моделей РВД за указанных период по существующим логам.'
