import os
import datetime
from pathlib import Path
from django.apps import AppConfig
from django.conf import settings
import logging
import shutil
from PIL import Image
import requests
from django.contrib.staticfiles.storage import staticfiles_storage

logger = logging.getLogger("todo_image_loader")

class TodoConfig(AppConfig):
    name = 'todo'
    verbose_name = "Django to do app, k8s demo"


    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def ready(self):
        self.loadStartUpPhoto()

    def loadStartUpPhoto(self):
        response = None
        logger.info("Starting to import photo.")
        image_path = f".{staticfiles_storage.url('images/start-up-photo.jpg')}"
        if Path(image_path).is_file():
            time_updated = self.modification_date(image_path)
            difference = datetime.datetime.now() - time_updated
            logger.info(f"Time difference: {difference}")
        if difference.total_seconds() / 3600 > 12:
            try:
                response = requests.get("https://picsum.photos/1200", stream=True)
                logger.info(f"Getting image status code: {response.status_code}")
                logger.info(f"{image_path}")
                with open(image_path, "wb") as output_file:
                    shutil.copyfileobj(response.raw, output_file)

            except Exception as error:
                logger.error(f"Loading photo failed: {error}")
            del response
        else:
            logger.info("Photo is updated within 12 hours.")


