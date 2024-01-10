from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE"))

bd_user = os.environ.get("DATABASE_USER")
db_password = os.environ.get("DATABASE_PASSWORD")
db_host = os.environ.get("DATABASE_HOST")
db_name = os.environ.get("DATABASE_NAME")

broker = f"sqla+mysql://{bd_user}:{db_password}@{db_host}/{db_name}"

app = Celery("server", broker=broker)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.imports = ("server.tasks", "accounts.tasks")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request), flush=True)