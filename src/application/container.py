from functools import lru_cache

from aiogram import Bot
from aiojobs import Scheduler
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from domain.repositories.ignored_messages import ABCIgnoredMessagesRepository
from domain.repositories.chats import ABCChatsRepository
from domain.repositories.skiped_messages import ABCSkipedMessagesRepository
from domain.services.message_moderation import MessageModerationService
from domain.utils.progress_counter_storage import ProgressCounterStorage

from infrastructure.proxy.report_proxy import ABCReportProxy, ReportProxy
from infrastructure.repositories.mongo.chats import MongoDBChatsRepository
from infrastructure.repositories.postgres.database import Database
from infrastructure.repositories.postgres.ignored_messages import PosgresIgnoredMessagesRepository
from infrastructure.repositories.postgres.skiped_messages import PosgresSkipedMessagesRepository
from infrastructure.utils.progress_counter_storage import ProgressCounterFileStorage

from settings.main import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb.connection_uri,
            serverSelectionTimeoutMS=3000,
        )
    
    def create_postgres_db():
        return Database(
            config.postgres.url
        )
    
    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    container.register(Database, factory=create_postgres_db, scope=Scope.singleton)

    database = container.resolve(Database)
    mongodb_client = container.resolve(AsyncIOMotorClient)

    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongodb_client=mongodb_client,
            mongodb_db_name=config.mongodb.database,
            mongodb_collection_name=config.mongodb.messages_collection,
        )
    
    def init_ignored_messages_postgres_repository() -> PosgresIgnoredMessagesRepository:
        return PosgresIgnoredMessagesRepository(
            database=database
        )
    
    def init_skiped_messages_postgres_repository() -> PosgresSkipedMessagesRepository:
        return PosgresSkipedMessagesRepository(
            database=database
        )

    # register repositiries
    container.register(
        ABCChatsRepository,
        factory=init_chats_mongodb_repository,
        scope=Scope.singleton
    )
    container.register(
        ABCIgnoredMessagesRepository,
        factory=init_ignored_messages_postgres_repository,
        scope=Scope.singleton
    )
    container.register(
        ABCSkipedMessagesRepository,
        factory=init_skiped_messages_postgres_repository,
        scope=Scope.singleton
    )

    def init_progress_counter_storage() -> ProgressCounterFileStorage:
        return ProgressCounterFileStorage(
            path=config.path_to_progress_counter,
        )
    
    #register storages
    container.register(
        ProgressCounterStorage,
        factory=init_progress_counter_storage,
        scope=Scope.singleton
    )

    def init_report_proxy() -> ReportProxy:
        return ReportProxy(
            bot=Bot(config.telegram_token),
            chat_id=config.telegram_id
        )

    # register proxy
    container.register(
        ABCReportProxy,
        factory=init_report_proxy,
        scope=Scope.singleton
    )

    def init_message_moderation_service() -> MessageModerationService:
        return MessageModerationService(
            chats_repo=container.resolve(ABCChatsRepository),
            ignored_messages_repo=container.resolve(ABCIgnoredMessagesRepository),
            skiped_messages_repo=container.resolve(ABCSkipedMessagesRepository),
            progress_counter_storage=container.resolve(ProgressCounterStorage),
            report_proxy=container.resolve(ABCReportProxy),
            num_records_per_req=config.num_records_per_req,
            num_repetitions_for_report=config.num_repetitions_for_report
        )

    # register service
    container.register(
        MessageModerationService,
        factory=init_message_moderation_service,
    )

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
