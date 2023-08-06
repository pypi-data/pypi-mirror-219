"""
This is where you can put handlers for running async background tasks

Task.Publish("myapp", "on_tq_test")
"""
# from datetime import datetime, timedelta
# from auditlog.models import PersistentLog
# from django.conf import settings
from incident.models import Event


def new_event(task):
    data = task.data
    if "hostname" in data.metadata:
        data.hostname = data.metadata.hostname
    if "details" in data.metadata:
        data.details = data.metadata.details
    if "component" in data.metadata:
        data.component = data.metadata.component
    if "component_id" in data.metadata:
        data.component_id = data.metadata.component_id
    if "ip" in data.metadata:
        data.reporter_ip = data.metadata.ip
    Event.createFromDict(None, task.data)
    task.completed()
