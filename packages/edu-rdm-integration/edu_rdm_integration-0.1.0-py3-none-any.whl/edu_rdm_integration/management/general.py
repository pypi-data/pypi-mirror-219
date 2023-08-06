import logging
from abc import (
    abstractmethod,
)
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
)

from django.conf import (
    settings,
)
from django.core.management import (
    CommandParser,
)
from django.core.management.base import (
    BaseCommand,
)

from edu_rdm_integration.consts import (
    DATETIME_FORMAT,
    REGIONAL_DATA_MART_INTEGRATION_COLLECTING_DATA,
    REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA,
)
from edu_rdm_integration.management.generators import (
    BaseEduLogGenerator,
)
from edu_rdm_integration.models import (
    RegionalDataMartEntityEnum,
    RegionalDataMartModelEnum,
)
from edu_rdm_integration.storages import (
    RegionalDataMartEntityStorage,
)
from educommon.audit_log.models import (
    AuditLog,
)
from function_tools.managers import (
    RunnerManager,
)


logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from django.core.management.base import (
        CommandParser,
    )


class BaseCollectModelDataCommand(BaseCommand):
    """
    Базовая команда для выполнения сбора данных моделей РВД.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Классы менеджеров Функций, которые должны быть запущены для сбора данных моделей РВД
        self._collecting_data_managers: Dict[str, Type[RunnerManager]] = dict()

        # Результаты работы Функций сбора данных моделей РВД
        self._collecting_data_results = []

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        models = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartModelEnum.get_enum_data().items()
        ])
        models_help_text = (
            f'Значением параметра является перечисление моделей РВД, для которых должен быть произведен сбор данных. '
            f'Перечисление моделей:\n{models}. Если модели не указываются, то сбор данных производится для всех '
            f'моделей. Модели перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--models',
            action='store',
            dest='models',
            type=(
                lambda e: tuple(
                    map(
                        lambda e_str: RegionalDataMartModelEnum.get_model_enum_value(e_str),
                        map(str.strip, e.split(','))
                    )
                )
            ),
            default=tuple(value for value in RegionalDataMartModelEnum.get_enum_data().values()),
            help=models_help_text,
        )

        parser.add_argument(
            '--logs_period_started_at',
            action='store',
            dest='logs_period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--logs_period_ended_at',
            action='store',
            dest='logs_period_ended_at',
            type=lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )

    def _find_collecting_models_data_managers(self, *args, **kwargs):
        """
        Поиск менеджеров Функций, которые должны быть запущены для сбора данных моделей РВД.
        """
        logger.info('collecting_models_data_managers..')

        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        collecting_models_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_COLLECTING_DATA},
        )

        for model_enum in kwargs.get('models'):
            manager_class = collecting_models_data_managers_map.get(model_enum.key)

            if manager_class:
                self._collecting_data_managers[model_enum.key] = manager_class

        logger.info('collecting models data managers finished')

    def _collect_models_data(self, *args, logs: Optional[Dict[str, List[AuditLog]]] = None, **kwargs):
        """
        Запуск Функций по формированию данных моделей РВД из логов.
        """
        logger.info('collect models data..')

        for model_key, manager_class in self._collecting_data_managers.items():
            model_logs = logs.get(model_key) if logs else None
            manager = manager_class(*args, logs=model_logs, **kwargs)
            manager.run()

            self._collecting_data_results.append(manager.result)

        logger.info('collecting entities data finished.')

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        logger.info(
            f'start collecting data of models - {", ".join([model.key for model in kwargs["models"]])}..'
        )

        self._find_collecting_models_data_managers(*args, **kwargs)
        self._collect_models_data(*args, **kwargs)

        logger.info('collecting models data finished.')


class BaseExportEntityDataCommand(BaseCommand):
    """
    Базовая команда для выполнения выгрузки данных сущностей РВД за указанный период.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Классы менеджеров Функций, которые должны быть запущены для выгрузки данных
        self._exporting_data_managers: Set[Type[RunnerManager]] = set()

        # Результаты работы Функций выгрузки данных
        self._exporting_data_results = []

        self._configure_agent_client()

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        entities = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartEntityEnum.get_enum_data().items()
        ])
        entities_help_text = (
            f'Значением параметра является перечисление сущностей РВД, для которых должена быть произведена выгрузка '
            f'данных. Перечисление сущностей:\n{entities}. Если сущности не указываются, то выгрузка данных '
            f'производится для всех сущностей. Сущности перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--entities',
            action='store',
            dest='entities',
            type=(
                lambda e: tuple(
                    map(
                        lambda e_str: RegionalDataMartEntityEnum.get_model_enum_value(e_str),
                        map(str.strip, e.split(','))
                    )
                )
            ),
            default=tuple(value for value in RegionalDataMartEntityEnum.get_enum_data().values()),
            help=entities_help_text,
        )

        parser.add_argument(
            '--period_started_at',
            action='store',
            dest='period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--period_ended_at',
            action='store',
            dest='period_ended_at',
            type=(
                lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT).replace(microsecond=time.max.microsecond)
            ),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )
        parser.add_argument(
            '--task_id',
            action='store',
            dest='task_id',
            type=str,
            default=None,
            help='task_id для поиска асинхронной задачи',
        )

    def _configure_agent_client(self):
        """
        Конфигурирование клиента загрузчика данных в Витрину.

        #TODO Вынужденная мера, т.к. при запуске команды не производится проверка готовности конфигов приложений.
          # Нужно переработать механизм конфигурирования клиента загрузчика.
        """
        import uploader_client
        from uploader_client.contrib.rdm.interfaces.configurations import (
            RegionalDataMartUploaderConfig,
        )
        if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    interface='uploader_client.contrib.rdm.interfaces.rest.OpenAPIInterfaceEmulation',
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=1,
                    request_retries=1,
                )
            )
        else:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=settings.RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT,
                    request_retries=settings.RDM_UPLOADER_CLIENT_REQUEST_RETRIES,
                )
            )

    def _find_exporting_entities_data_managers(self, *args, **kwargs):
        """
        Поиск менеджеров Функций выгрузки данных по сущностям РВД.
        """
        logger.info('find exporting entities data manager..')

        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        exporting_entities_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )

        for entity in kwargs.get('entities'):
            manager_class = exporting_entities_data_managers_map.get(entity.key)

            if manager_class:
                self._exporting_data_managers.add(manager_class)

        logger.info('finding exporting entities data manager finished.')

    def _export_entities_data(self, *args, **kwargs):
        """
        Выгрузка данных по указанным сущностям.
        """
        logger.info('start exporting entities data..')

        for manager_class in self._exporting_data_managers:
            manager = manager_class(*args, is_only_main_model=True, **kwargs)
            manager.run()

            self._exporting_data_results.append(manager.result)

        logger.info('exporting entities data finished.')

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        logger.info(
            f'start exporting data of entities - {", ".join([entity.key for entity in kwargs["entities"]])}..'
        )

        self._find_exporting_entities_data_managers(*args, **kwargs)
        self._export_entities_data(*args, **kwargs)

        logger.info('exporting entities data finished.')


class BaseCollectModelsDataByGeneratingLogsCommand(BaseCollectModelDataCommand):
    """
    Команда сбора данных моделей РВД на основе существующих в БД данных моделей ЭШ.

    Можно регулировать, для каких моделей должен быть произведен сбор данных, и период, за который должны
    быть собраны логи. Логи формируются в процессе выполнения команды при помощи генератора логов LogGenerator для
    указанной модели.
    """

    # flake8: noqa: A003
    help = 'Команда сбора данных моделей РВД на основе существующих в БД данных моделей продукта'

    def __init__(self, *args, **kwargs):
        """Инициализация команды."""
        super().__init__(*args, **kwargs)

        self.log_generator = self.prepare_log_generator()

    @abstractmethod
    def prepare_log_generator(self) -> 'BaseEduLogGenerator':
        """Возвращает генератор логов."""

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        super().add_arguments(parser=parser)

        parser.add_argument(
            '--logs_sub_period_days',
            action='store',
            dest='logs_sub_period_days',
            type=int,
            default=0,
            help=(
                'Размер подпериодов, на которые будет разбит основной период, в днях. По умолчанию, '
                '0 - разбиение на подпериоды отключено.'
            ),
        )

        parser.add_argument(
            '--school_ids',
            action='store',
            dest='school_ids',
            type=lambda v: tuple(map(int, v.split(','))),
            default=(),
            help='Школы, для которых производится выгрузка.',
        )

    def _generate_logs_by_subperiod(self, *args, **kwargs):
        """
        Генерация логов с учетом подпериодов.
        """
        logs_period_started_at = kwargs.get('logs_period_started_at')
        logs_period_ended_at = kwargs.get('logs_period_ended_at')
        school_ids = kwargs.get('school_ids')

        temp_logs_period_started_at = logs_period_started_at
        temp_logs_period_ended_at = logs_period_started_at + timedelta(days=kwargs.get('logs_sub_period_days'))

        if temp_logs_period_ended_at > logs_period_ended_at:
            temp_logs_period_ended_at = logs_period_ended_at

        temp_logs: Dict[str, List[AuditLog]] = dict()

        while temp_logs_period_started_at < temp_logs_period_ended_at <= logs_period_ended_at:
            for model in kwargs.get('models'):
                logs = self.log_generator.generate(
                    model=model,
                    logs_period_started_at=temp_logs_period_started_at,
                    logs_period_ended_at=temp_logs_period_ended_at,
                    school_ids=school_ids,
                )

                temp_logs[model.key] = logs

            yield temp_logs, temp_logs_period_started_at, temp_logs_period_ended_at

            temp_logs_period_started_at = temp_logs_period_ended_at
            temp_logs_period_ended_at += timedelta(days=kwargs.get('logs_sub_period_days'))

            if temp_logs_period_ended_at > logs_period_ended_at:
                temp_logs_period_ended_at = logs_period_ended_at

            temp_logs.clear()

    def _generate_logs_for_all_period(self, *args, **kwargs):
        """
        Генерация логов за весь период.
        """
        logs_period_started_at = kwargs.get('logs_period_started_at')
        logs_period_ended_at = kwargs.get('logs_period_ended_at')
        school_ids = kwargs.get('school_ids')

        temp_logs: Dict[str, List[AuditLog]] = dict()

        for model in kwargs.get('models'):
            logs = self.log_generator.generate(
                model=model,
                logs_period_started_at=logs_period_started_at,
                logs_period_ended_at=logs_period_ended_at,
                school_ids=school_ids,
            )

            temp_logs[model.key] = logs

        return [(temp_logs, logs_period_started_at, logs_period_ended_at)]

    def _generate_logs(self, *args, **kwargs) -> List[Tuple[Dict[str, List[AuditLog]], datetime, datetime]]:
        """
        Генерация логов.

        Осуществляет генерацию логов по уже существующим записям в базе данных. В качестве параметров указываются
        начало и конец периода сбора логов, размер подпериодов, на которые должен быть разбит основной период.
        Генерация логов производится только для указанных моделей.
        """
        if kwargs.get('logs_sub_period_days'):
            logs = self._generate_logs_by_subperiod(*args, **kwargs)
        else:
            logs = self._generate_logs_for_all_period(*args, **kwargs)

        return logs

    def handle(self, *args, **kwargs):
        """
        Запуск сбора данных указанных моделей РВД на основе существующих данных моделей ЭШ.
        """
        logger.info(
            f'start collecting data of models - {", ".join([model.key for model in kwargs["models"]])}..'
        )

        self._find_collecting_models_data_managers(*args, **kwargs)

        temp_kwargs = kwargs.copy()

        for logs, logs_period_started_at, logs_period_ended_at in self._generate_logs(*args, **kwargs):
            temp_kwargs['logs_period_started_at'] = logs_period_started_at
            temp_kwargs['logs_period_ended_at'] = logs_period_ended_at

            self._collect_models_data(*args, logs=logs, **temp_kwargs)

        logger.info('collecting models data finished.')
