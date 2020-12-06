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

    def ready(self):
        self.loadStartUpPhoto()

    # https://www.geeksforgeeks.org/python-uploading-images-in-django/
    def loadStartUpPhoto(self):
        response = None
        logger.info("Starting to import photo.")
        try:
            response = requests.get("https://picsum.photos/1200", stream=True)
            logger.info(f"Getting image status code: {response.status_code}")
            image_path = f".{staticfiles_storage.url('images/start-up-photo.jpg')}"
            logger.info(f"{image_path}")
            with open(image_path, "wb") as output_file:
                shutil.copyfileobj(response.raw, output_file)

        except Exception as error:
            logger.error(f"Loading photo failed: {error}")
        del response


