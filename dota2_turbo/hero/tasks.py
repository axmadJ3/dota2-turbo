import logging

from celery import shared_task

from dota2_turbo.hero.services.update_heroes_stats import update_heroes_stats
from dota2_turbo.hero.services.update_heroes_facets import update_heroes_facets


logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def update_heroes():
    logger.info("Start updating heroes")
    result = update_heroes_stats()
    logger.info(f"Total updated {result}")
    return result


@shared_task(
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def update_facets():
    logger.info("Start updating facets")
    result = update_heroes_facets()
    logger.info(f"Total updated {result}")
    return result
