#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from celery import Celery
import celery_aio_pool as aio_pool

# local
from app.common import constants


assert aio_pool.patch_celery_tracer() is True

celery = Celery("Chaoxing_Celery",
                worker_pool=aio_pool.pool.AsyncIOPool,
                CELERY_ACCEPT_CONTENT=['pickle', ])
celery.conf.broker_url = constants.CELERY_BROKER_URL
celery.conf.result_backend = constants.CELERY_RESULT_BACKEND


celery.autodiscover_tasks(['app.modules.chaoxing'])



