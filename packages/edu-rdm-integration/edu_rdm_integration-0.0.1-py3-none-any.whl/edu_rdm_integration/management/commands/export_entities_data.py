from edu_rdm_integration.management.general import (
    BaseExportEntityDataCommand,
)


class Command(BaseExportEntityDataCommand):
    """
    Команда для выгрузки данных сущностей РВД.
    """

    # flake8: noqa: A003
    help = 'Команда для выгрузки данных сущностей РВД за указанных период.'
