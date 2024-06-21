import logging
from ..extensions import db
from ..models import Drone

logger = logging.getLogger(__name__)

class DroneService:
    @staticmethod
    def get_all_drones(page, per_page):
        try:
            drones = Drone.query.paginate(page=page, per_page=per_page, error_out=False)
            logger.debug("Drones fetched successfully!")
            return drones
        except Exception as e:
            logger.error(f"Error fetching drones: {str(e)}")
            return None

    @staticmethod
    def seed_initial_drones():
        try:
            existing_drones_count = Drone.query.count()
            if existing_drones_count < 10:
                for i in range(10 - existing_drones_count):
                    drone = Drone(name=f'Drone {i+1}')
                    db.session.add(drone)
                db.session.commit()
                logger.debug(f"Seeded {10 - existing_drones_count} drones.")
        except Exception as e:
            logger.error(f"Error seeding drones: {str(e)}")
