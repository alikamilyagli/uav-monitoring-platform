import logging
import io
import random
from PIL import Image as PILImage
from flask import current_app
from random import randint
from ..minio_utils import MinioUtils
from ..models import Task, Image, Drone
from ..extensions import db

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    def get_all_tasks(page, per_page):
        try:
            tasks = Task.query.paginate(page=page, per_page=per_page, error_out=False)
            logger.debug("Tasks fetched successfully!")
            return tasks
        except Exception as e:
            logger.error(f"Error fetching tasks: {str(e)}")
            return None

    @staticmethod
    def create_task(data):
        try:
            drone_ids = data.get('drone_ids', [])
            drones = Drone.query.filter(Drone.id.in_(drone_ids)).all()
            task = Task(name=data['name'], description=data.get('description'))
            for drone in drones:
                task.drones.append(drone)
            db.session.add(task)
            db.session.commit()
            logger.debug(f"Task created with id: {str(task.id)}")
            return task
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return None

    @staticmethod
    def update_task(task_id, data):
        try:
            task = Task.query.get_or_404(task_id)
            task.name = data.get('name', task.name)
            task.description = data.get('description', task.description)

            drone_ids = data.get('drone_ids', [])
            drones = Drone.query.filter(Drone.id.in_(drone_ids)).all()
            task.drones = drones

            db.session.commit()
            logger.debug(f"Task updated with id: {str(task.id)}")
            return task
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            return None

    @staticmethod
    def get_task(task_id):
        try:
            task = Task.query.get_or_404(task_id)
            logger.debug(f"Task fetched with id: {str(task.id)}")
            return task
        except Exception as e:
            logger.error(f"Error fetching task: {str(e)}")
            return None

    @staticmethod
    def execute_task(task_id):
        try:
            minio_utils = MinioUtils(
                current_app.config['MINIO_ENDPOINT'],
                current_app.config['MINIO_ACCESS_KEY'],
                current_app.config['MINIO_SECRET_KEY']
            )

            task = Task.query.get_or_404(task_id)

            for drone in task.drones:
                for i in range(5):
                    image_data = generate_tiny_image()
                    image_name = f'task_{task.id}_drone_{drone.id}_image_{i}.png'

                    if not minio_utils.upload_image('uav-images', image_name, image_data):
                        current_app.logger.error(f"Failed to upload image {image_name} for task {task_id}")
                        return None

                    # Create and add Image object to session
                    image = Image(task_id=task.id, image_name=image_name, drone_id=drone.id)
                    db.session.add(image)

            db.session.commit()
            current_app.logger.debug(f"Task executed with id: {str(task.id)}")
            return task

        except Exception as e:
            current_app.logger.error(f"Error executing task: {str(e)}")
            return None


    @staticmethod
    def get_task_images(task_id):
        try:
            minio_utils = MinioUtils(
                current_app.config['MINIO_ENDPOINT'],
                current_app.config['MINIO_ACCESS_KEY'],
                current_app.config['MINIO_SECRET_KEY']
            )

            task = Task.query.get_or_404(task_id)
            # images = task.images
            images = sorted(task.images, key=lambda x: x.capture_date, reverse=True)

            image_data = [
                {
                    "image_url": minio_utils.get_image_url('uav-images', image.image_name),
                    "capture_date": image.capture_date.isoformat(),
                    "drone_id": image.drone_id
                }
                for image in images
            ]

            logger.debug(f"Task images fetched with id: {str(task_id)}")
            return image_data

        except Exception as e:
            logger.error(f"Error fetching task images: {str(e)}")
            return None


def generate_tiny_image():
    image = PILImage.new('RGB', (10, 10))
    pixels = image.load()

    for x in range(image.width):
        for y in range(image.height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels[x, y] = (r, g, b)

    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_data.seek(0)
    return image_data