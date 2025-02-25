from functools import lru_cache

from aiogram import Bot
from aiojobs import Scheduler
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from redis.asyncio import Redis

from domain.repositories.ignored_messages import ABCIgnoredMessagesRepository
from domain.repositories.messages import ABCMessagesRepository
from domain.services.message_moderation import MessageModerationService
from domain.utils.progress_counter_storage import ProgressCounterStorage
from domain.utils.skiped_message_ids_storage import SkipedMessageIdsStorage

from infrastructure.proxy.report_proxy import ABCReportProxy, ReportProxy
from infrastructure.repositories.mongo.messages import MongoDBMessagesRepository
from infrastructure.repositories.redis.ignored_messages import RedisIgnoredMessagesRepository
from infrastructure.utils.progress_counter_storage import ProgressCounterRedisStorage
from infrastructure.utils.skiped_message_ids_storage import SkipedMessageIdsRedisStorage

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
    
    def create_redis_client():
        return Redis.from_url(config.redis.url)
    
    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    container.register(Redis, factory=create_redis_client, scope=Scope.singleton)
    
    redis_client = container.resolve(Redis)
    mongodb_client = container.resolve(AsyncIOMotorClient)

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongodb_client=mongodb_client,
            mongodb_db_name=config.mongodb.database,
            mongodb_collection_name=config.mongodb.messages_collection,
        )
    
    def init_ignored_messages_redis_repository() -> RedisIgnoredMessagesRepository:
        return RedisIgnoredMessagesRepository(
            client=redis_client,
            prefix="ignored_messages",
        )

    # register repositiries
    container.register(
        ABCMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton
    )
    container.register(
        ABCIgnoredMessagesRepository,
        factory=init_ignored_messages_redis_repository,
        scope=Scope.singleton
    )

    def init_progress_counter_storage() -> ProgressCounterRedisStorage:
        return ProgressCounterRedisStorage(
            client=redis_client,
        )
    
    def init_skiped_messages_ids_storage() -> SkipedMessageIdsRedisStorage:
        return SkipedMessageIdsRedisStorage(
            client=redis_client,
        )

    #register storages
    container.register(
        ProgressCounterStorage,
        factory=init_progress_counter_storage,
        scope=Scope.singleton
    )
    container.register(
        SkipedMessageIdsStorage,
        factory=init_skiped_messages_ids_storage,
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
            messages_repo=container.resolve(ABCMessagesRepository),
            ignored_messages_repo=container.resolve(ABCIgnoredMessagesRepository),
            progress_counter_storage=container.resolve(ProgressCounterStorage),
            skiped_message_ids_storage=container.resolve(SkipedMessageIdsStorage),
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
