from rest import decorators as rd
from datetime import datetime, timedelta
from taskqueue.models import Task
from .models import Metrics
from rest import log


@rd.periodic(minute=15, hour=10)
def run_cleanup(force=False, verbose=False, now=None):
    count = Metrics.objects.filter(expires__lte=datetime.now()).delete()
    if count > 0:
        logger = log.getLogger("auditlog", filename="auditlog.log")
        logger.info(f"METRICS.CLEANUP {count} expired records deleted")

