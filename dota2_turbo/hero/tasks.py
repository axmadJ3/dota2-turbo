import logging

from celery import shared_task

from dota2_turbo.hero.services.update_heroes_stats import update_heroes_stats 


logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backofs=5,
    retry_kwargs={"max_retries": 3},
)
def update_heroes():
    logger.info("Start updating heroes")
    result = update_heroes_stats()
    logger.info(f"Total updated {result}")
    return result
